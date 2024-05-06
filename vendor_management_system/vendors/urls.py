from django.urls import path
from .views import VendorListCreate, VendorRetrieveUpdateDestroy

urlpatterns = [
    path('api/vendors/', VendorListCreate.as_view()),
    path('api/vendors/<str:vendor_code>/',
         VendorRetrieveUpdateDestroy.as_view()),
]
