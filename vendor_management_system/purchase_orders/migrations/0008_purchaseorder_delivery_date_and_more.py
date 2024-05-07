# Generated by Django 5.0.4 on 2024-05-06 19:15

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purchase_orders', '0007_purchaseorder_quality_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchaseorder',
            name='delivery_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='purchaseorder',
            name='expected_delivery_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 6, 19, 15, 39, 542148, tzinfo=datetime.timezone.utc)),
            preserve_default=False,
        ),
    ]
