from django.urls import path
from .views import *

urlpatterns = [
    path('code/', ValidatePromocodeView.as_view(), name='validate_promocode'),
    path('register/', UserRegistrationView.as_view(), name='user_registration'),
]