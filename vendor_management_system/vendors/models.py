from django.db import models


class Vendor(models.Model):
    name = models.CharField(max_length=100)
    contact_details = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    vendor_code = models.CharField(max_length=50, primary_key=True)

    def __str__(self):
        return self.name
