from django.dispatch import Signal, receiver
from django.db.models.signals import post_save
from .models import PurchaseOrder
from django.db.models import F

recalculate_avg_response_time_signal = Signal()


@receiver(recalculate_avg_response_time_signal)
def recalculate_avg_response_time(sender, vendor, **kwargs):
    vendor_purchase_orders = PurchaseOrder.objects.filter(
        vendor=vendor, acknowledgment_date__isnull=False)

    total_response_time = sum((order.acknowledgment_date - order.issue_date).total_seconds()
                              for order in vendor_purchase_orders)
    number_of_orders = vendor_purchase_orders.count()

    if number_of_orders > 0:
        average_response_time = total_response_time / number_of_orders

        vendor.average_response_time = average_response_time
        vendor.save()


@receiver(post_save, sender=PurchaseOrder)
def recalculate_fullfilment_rate(sender, instance: PurchaseOrder, **kwargs):
    if instance.status.lower() == 'completed':
        vendor = instance.vendor
        total_orders = PurchaseOrder.objects.filter(
            vendor=instance.vendor).count()
        if total_orders > 0:
            completed_orders = PurchaseOrder.objects.filter(
                vendor=instance.vendor, status__iexact='completed').count()
            vendor.fulfilment_rate = completed_orders/total_orders*100
            vendor.save()


@receiver(post_save, sender=PurchaseOrder)
def recalculate_avg_quality_rating(sender, instance: PurchaseOrder, **kwargs):
    if instance.status.lower() == 'completed' and instance.quality_rating:
        vendor = instance.vendor
        rated_pos = PurchaseOrder.objects.filter(
            vendor=vendor, quality_rating__isnull=False)
        if rated_pos.count() > 0:
            total_rating = sum(
                rated_po.quality_rating for rated_po in rated_pos)
            vendor.quality_rating_avg = total_rating/rated_pos.count()
            vendor.save()


@receiver(post_save, sender=PurchaseOrder)
def recalculate_on_time_delivery_rate(sender, instance: PurchaseOrder, **kwargs):
    if instance.status.lower() == 'completed' and instance.delivery_date:
        vendor = instance.vendor
        on_time_pos = PurchaseOrder.objects.filter(
            vendor=vendor, status__iexact='completed', expected_delivery_date__gte=F('delivery_date')).count()
        total_completed_pos = PurchaseOrder.objects.filter(
            vendor=vendor, status__iexact='completed').count()
        if total_completed_pos > 0:
            on_time_delivery_rate = on_time_pos/total_completed_pos*100
            vendor.on_time_delivery_rate = on_time_delivery_rate
            vendor.save()
