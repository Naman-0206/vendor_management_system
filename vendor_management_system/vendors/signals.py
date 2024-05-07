from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Vendor, HistoricalPerformance
from django.utils import timezone
from django.conf import settings


@receiver(post_save, sender=Vendor)
def add_vendor_metrics_to_historical(sender, instance: Vendor, created, **kwargs):
    create_new_record = True
    update_old_record = False

    last_record = HistoricalPerformance.objects.filter(
        vendor=instance).order_by('-date').first()

    if last_record:
        time_difference = timezone.now() - last_record.date
        delay_time_seconds = getattr(
            settings, 'HISTORICAL_RECORD_DELAY_SECONDS')

        create_new_record = time_difference.total_seconds() >= delay_time_seconds
        update_old_record = time_difference.total_seconds() <= 10

    if create_new_record:
        HistoricalPerformance.objects.create(
            vendor=instance,
            on_time_delivery_rate=instance.on_time_delivery_rate,
            quality_rating_avg=instance.quality_rating_avg,
            average_response_time=instance.average_response_time,
            fulfilment_rate=instance.fulfilment_rate
        )

    elif update_old_record:
        old_record = HistoricalPerformance.objects.filter(
            vendor=instance).order_by('-date').first()
        if old_record:
            old_record.on_time_delivery_rate = instance.on_time_delivery_rate
            old_record.quality_rating_avg = instance.quality_rating_avg
            old_record.average_response_time = instance.average_response_time
            old_record.fulfilment_rate = instance.fulfilment_rate
            old_record.save()
