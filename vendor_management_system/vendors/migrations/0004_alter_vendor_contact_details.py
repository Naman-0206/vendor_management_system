# Generated by Django 5.0.4 on 2024-05-06 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendors', '0003_vendor_average_response_time_vendor_fulfilment_rate_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendor',
            name='contact_details',
            field=models.TextField(),
        ),
    ]
