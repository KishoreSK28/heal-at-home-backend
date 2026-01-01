from django.db import models


class Service(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class PhysiotherapistAvailability(models.Model):
    date = models.DateField(unique=True)
    is_available = models.BooleanField(default=False)

    available_from = models.TimeField(null=True, blank=True)
    available_to = models.TimeField(null=True, blank=True)
    manually_closed = models.BooleanField(default=False)


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # ✅ REQUIRED

    def __str__(self):
        return f"{self.date} - {'Available' if self.is_available else 'Not Available'}"

class AppointmentRequest(models.Model):
    SERVICE_CHOICES = [
        ('general', 'General Query'),
        ('elderly', 'Elderly Care'),
        ('ortho', 'Orthopedic Physiotherapy'),
        ('neuro', 'Neuro Rehabilitation'),
        ('post_surgery', 'Post Surgery Rehab'),
    ]

    full_name = models.CharField(max_length=120)
    phone_number = models.CharField(max_length=15)
    service = models.CharField(max_length=50, choices=SERVICE_CHOICES)
    message = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    is_contacted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.full_name} - {self.get_service_display()}"
