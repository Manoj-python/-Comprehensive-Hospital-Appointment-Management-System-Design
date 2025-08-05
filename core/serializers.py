from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *

class HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = '__all__'

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class DoctorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorProfile
        fields = '__all__'

class DoctorAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorAvailability
        fields = '__all__'

class PatientProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientProfile
        fields = '__all__'
from rest_framework import serializers
from .models import Appointment
from decimal import Decimal

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'

    def create(self, validated_data):
        amount = validated_data['amount_paid']  # This is DecimalField
        validated_data['doctor_share'] = amount * Decimal('0.6')
        validated_data['hospital_share'] = amount * Decimal('0.4')
        return super().create(validated_data)
