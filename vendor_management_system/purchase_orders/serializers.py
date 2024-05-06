from rest_framework import serializers
from .models import PurchaseOrder


class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = ['po_number', 'vendor', 'order_date',
                  'items', 'quantity', 'status']
