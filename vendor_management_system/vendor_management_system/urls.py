from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('vendors.urls')),
    path('', include('purchase_orders.urls')),
    path('', include('auth.urls')),
]
