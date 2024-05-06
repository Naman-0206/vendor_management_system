from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Vendor
from .serializers import VendorPerformanceSerializer


class VendorProfileTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.vendor = Vendor.objects.create(
            name='Test Vendor',
            contact_details='test@example.com',
            address='123 Test St',
            vendor_code='TEST1234'
        )
        self.initial_vendor_count = Vendor.objects.count()

    def test_create_vendor(self):
        response = self.client.post('/api/vendors/', {
            'name': 'Test Vendor',
            'contact_details': 'test@example.com',
            'address': '123 Test St',
            'vendor_code': 'TEST123'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Vendor.objects.count(), self.initial_vendor_count+1)
        self.assertEqual(Vendor.objects.get(pk='TEST123').name, 'Test Vendor')

    def test_list_vendors(self):
        response = self.client.get('/api/vendors/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), self.initial_vendor_count)

        Vendor.objects.create(
            name='Test Vendor',
            contact_details='test@example.com',
            address='123 Test St',
            vendor_code='TEST123'
        )

        response = self.client.get('/api/vendors/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), self.initial_vendor_count+1)

    def test_retrieve_vendor(self):
        vendor = Vendor.objects.create(
            name='Test Vendor',
            contact_details='test@example.com',
            address='123 Test St',
            vendor_code='TEST123'
        )
        response = self.client.get(f'/api/vendors/{vendor.vendor_code}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Vendor')

    def test_update_vendor(self):
        vendor = Vendor.objects.create(
            name='Test Vendor',
            contact_details='test@example.com',
            address='123 Test St',
            vendor_code='TEST123'
        )
        updated_data = {
            'name': 'Updated Vendor',
            'contact_details': 'updated_test@example.com',
            'address': '456 Updated St',
            'vendor_code': 'TEST123'
        }
        response = self.client.put(
            f'/api/vendors/{vendor.vendor_code}/', updated_data)
        self.assertEqual(response.status_code,
                         status.HTTP_200_OK, msg=response.data)
        vendor.refresh_from_db()
        self.assertEqual(vendor.name, 'Updated Vendor', msg=response.data)

    def test_delete_vendor(self):
        vendor = Vendor.objects.create(
            name='Test Vendor',
            contact_details='test@example.com',
            address='123 Test St',
            vendor_code='TEST123'
        )
        response = self.client.delete(f'/api/vendors/{vendor.vendor_code}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Vendor.objects.count(), self.initial_vendor_count)

    def test_get_vendor_performance(self):
        response = self.client.get(
            f'/api/vendors/{self.vendor.pk}/performance/')
        serializer = VendorPerformanceSerializer(self.vendor)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
