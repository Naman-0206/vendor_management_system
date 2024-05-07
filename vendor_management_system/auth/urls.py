from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import RegisterUser

urlpatterns = [
    path('api/token/', obtain_auth_token),
    path('api/register/', RegisterUser.as_view()),
]
