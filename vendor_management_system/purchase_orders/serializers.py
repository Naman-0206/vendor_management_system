from rest_framework import serializers
from .models import PurchaseOrder


class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = ['po_number', 'vendor', 'order_date', 'issue_date',
                  'items', 'quantity', 'status', 'quality_rating', 'expected_delivery_date', 'delivery_date']

    def validate(self, data):
        status = data.get('status')
        delivery_date = data.get('delivery_date')

        if status == 'completed' and delivery_date is None:
            raise serializers.ValidationError(
                {'delivery_date': 'Delivery date cannot be null for completed orders.'})

        return data


class AcknowledgePurchaseOrderSerializer(serializers.Serializer):
    pass
