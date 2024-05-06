from django.dispatch import Signal, receiver
from .models import PurchaseOrder

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
