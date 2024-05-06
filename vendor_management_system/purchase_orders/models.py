from django.db import models
from vendors.models import Vendor
from django.core.validators import MinValueValidator, MaxValueValidator


class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=100, primary_key=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    items = models.JSONField()
    quantity = models.PositiveIntegerField()
    status = models.CharField(max_length=50, default="Order Placed")
    issue_date = models.DateTimeField()

    acknowledgment_date = models.DateTimeField(null=True)

    quality_rating = models.FloatField(
        null=True, validators=[MinValueValidator(0), MaxValueValidator(5)])

    def __str__(self):
        return self.po_number
