from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from datetime import date, datetime, time
from urllib.parse import quote_plus
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import Service, PhysiotherapistAvailability, AppointmentRequest
from .serializers import (
    ServiceSerializer,
    AvailabilitySerializer,
    AppointmentRequestSerializer,
)

# ======================================================
# PRIVATE ADMIN VIEWS
# ======================================================

@login_required
def save_availability(request):
    today = date.today()

    is_available = request.POST.get('is_available') == 'on'
    from_time = request.POST.get('available_from') or None
    to_time = request.POST.get('available_to') or None

    PhysiotherapistAvailability.objects.update_or_create(
        date=today,
        defaults={
            'is_available': is_available,
            'available_from': from_time if is_available else None,
            'available_to': to_time if is_available else None,
            'manually_closed': not is_available,  # 👈 KEY LINE
        }
    )

    return redirect('availability')

def admin_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user and user.is_superuser:
            login(request, user)
            return redirect('dashboard')

        return render(request, 'admin_panel/login.html', {
            'error': 'Invalid credentials'
        })

    return render(request, 'admin_panel/login.html')


@login_required
def dashboard(request):
    today = date.today()

    total_appointments = AppointmentRequest.objects.count()
    pending_requests = AppointmentRequest.objects.filter(
        is_contacted=False
    ).count()

    availability = PhysiotherapistAvailability.objects.filter(
        date=today
    ).order_by('-id').first()

    is_available = availability.is_available if availability else False

    return render(request, 'admin_panel/dashboard.html', {
        'total_appointments': total_appointments,
        'pending_requests': pending_requests,
        'is_available': is_available,
    })



@login_required
def appointments(request):
    appointments = AppointmentRequest.objects.order_by('-created_at')

    for a in appointments:
        message = f"""
Hello {a.full_name},

This is *HealAtHome Physio* confirming your appointment request:

Service:
{a.get_service_display()}

Your Message:
{a.message}

We received your request and will contact you shortly.

– HealAtHome Physio Team
"""

        # 🔑 THIS LINE IS CRITICAL
        a.wa_text = quote_plus(message)

    return render(request, 'admin_panel/appointments.html', {
        'appointments': appointments,
    })

@login_required
def delete_appointment(request, appointment_id):
    if request.method == 'POST':
        appointment = get_object_or_404(AppointmentRequest, id=appointment_id)
        appointment.delete()
    return redirect('appointments')


@login_required
def availability(request):
    today = date.today()
    today_availability = PhysiotherapistAvailability.objects.filter(
        date=today
    ).order_by('-id').first()

    data = PhysiotherapistAvailability.objects.order_by('-date')

    return render(request, 'admin_panel/availability.html', {
        'availability': data,
        'today': today_availability,  # 👈 IMPORTANT
    })







@login_required
def toggle_contacted(request, appointment_id):
    if request.method != 'POST':
        return redirect('appointments')

    appointment = get_object_or_404(AppointmentRequest, id=appointment_id)
    appointment.is_contacted = not appointment.is_contacted
    appointment.save()
    return redirect('appointments')






def admin_logout(request):
    logout(request)
    return redirect('admin_login')

# ======================================================
# PUBLIC API VIEWS (FLUTTER)
# ======================================================

@api_view(['GET'])
@permission_classes([AllowAny])
def services_list(request):
    """
    Public: Only active services
    """
    services = Service.objects.filter(is_active=True)
    serializer = ServiceSerializer(services, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def today_availability(request):
    today = date.today()
    now = datetime.now().time()

    availability = PhysiotherapistAvailability.objects.filter(
        date=today
    ).order_by('-id').first()

    if not availability:
        return Response({
            'date': str(today),
            'is_available': False,
        })

    # 🔴 Manual close overrides everything
    if availability.manually_closed:
        return Response({
            'date': str(today),
            'is_available': False,
        })

    # ⏰ Time-based auto expiry
    if availability.available_from and availability.available_to:
        if not (availability.available_from <= now <= availability.available_to):
            return Response({
                'date': str(today),
                'is_available': False,
            })

    return Response({
        'date': str(today),
        'is_available': availability.is_available,
    })


@api_view(['POST'])
@permission_classes([AllowAny])
def create_appointment(request):
    """
    Public: Appointment / Contact form submission
    """
    serializer = AppointmentRequestSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(
            {'message': 'Appointment request submitted'},
            status=status.HTTP_201_CREATED
        )

    # Debug-friendly (remove in production)
    print(serializer.errors)

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )
