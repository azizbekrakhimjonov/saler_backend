from django.urls import path
from .views import *

urlpatterns = [
    path('api/', ValidatePromocodeView.as_view(), name='validate_promocode'),
]