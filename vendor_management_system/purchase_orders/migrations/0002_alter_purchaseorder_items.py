# Generated by Django 5.0.4 on 2024-05-06 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purchase_orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseorder',
            name='items',
            field=models.JSONField(),
        ),
    ]
