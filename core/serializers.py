from rest_framework import serializers
from .models import Service, PhysiotherapistAvailability, AppointmentRequest


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'name', 'description']


class AvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = PhysiotherapistAvailability
        fields = ['date', 'is_available', 'available_from', 'available_to']


class AppointmentRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppointmentRequest
        fields = '__all__'
