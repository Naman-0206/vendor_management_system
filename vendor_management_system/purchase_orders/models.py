from django.db import models
from vendors.models import Vendor


class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=100, primary_key=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    items = models.JSONField()
    quantity = models.PositiveIntegerField()
    status = models.CharField(max_length=50, default="Order Placed")

    acknowledgment_date = models.DateTimeField(null=True)

    def __str__(self):
        return self.po_number
