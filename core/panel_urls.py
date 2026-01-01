from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.admin_login, name='admin_login'),
    path('logout/', views.admin_logout, name='admin_logout'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('appointments/', views.appointments, name='appointments'),
    path('availability/', views.availability, name='availability'),
    path('availability/save/', views.save_availability, name='save_availability'),
    path(
    'appointments/delete/<int:appointment_id>/',
    views.delete_appointment,
    name='delete_appointment'
),
    path('appointments/toggle/<int:appointment_id>/', views.toggle_contacted, name='toggle_contacted'),


]
