from django.contrib import admin
from .models import (
    Hospital,
    Department,
    DoctorProfile,
    DoctorAvailability,
    PatientProfile,
    Appointment,
)

@admin.register(Hospital)
class HospitalAdmin(admin.ModelAdmin):
    list_display = ('name', 'location')
    search_fields = ('name', 'location')


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'hospital')
    list_filter = ('hospital',)
    search_fields = ('name',)


@admin.register(DoctorProfile)
class DoctorProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'qualifications', 'experience')
    search_fields = ('name', 'specializations', 'qualifications')
    autocomplete_fields = ['user']


@admin.register(DoctorAvailability)
class DoctorAvailabilityAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'hospital', 'date', 'start_time', 'end_time', 'consultation_fee')
    list_filter = ('hospital', 'date')
    autocomplete_fields = ['doctor', 'hospital']


@admin.register(PatientProfile)
class PatientProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'gender', 'date_of_birth', 'unique_id')
    search_fields = ('name', 'unique_id')
    autocomplete_fields = ['user']


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'hospital', 'date', 'time', 'amount_paid')
    list_filter = ('hospital', 'date')
    autocomplete_fields = ['patient', 'doctor', 'hospital']
