from django.urls import path
from .views import (
    services_list,
    today_availability,
    create_appointment,
)

urlpatterns = [
    path('services/', services_list),
    path('availability/today/', today_availability),
    path('appointment/', create_appointment, name='create_appointment'),
]
