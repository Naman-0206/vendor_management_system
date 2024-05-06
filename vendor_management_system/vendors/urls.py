from django.urls import path
from .views import VendorListCreate, VendorRetrieveUpdateDestroy, VendorPerformance

urlpatterns = [
    path('api/vendors/', VendorListCreate.as_view()),
    path('api/vendors/<str:vendor_code>/',
         VendorRetrieveUpdateDestroy.as_view()),
    path('api/vendors/<str:vendor_code>/performance/',
         VendorPerformance.as_view()),
]
