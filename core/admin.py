from django.contrib import admin
from .models import Service, PhysiotherapistAvailability, AppointmentRequest


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)


@admin.register(PhysiotherapistAvailability)
class AvailabilityAdmin(admin.ModelAdmin):
    list_display = ('date', 'is_available', 'available_from', 'available_to')
    list_filter = ('is_available',)
    ordering = ('-date',)


@admin.register(AppointmentRequest)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = (
        'full_name',
        'phone_number',
        'service',
        'created_at',
        'is_contacted',
    )
    list_filter = ('service', 'is_contacted')
    search_fields = ('full_name', 'phone_number')
