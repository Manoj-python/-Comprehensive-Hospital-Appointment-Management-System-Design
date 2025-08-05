from django.db import models
from django.contrib.auth.models import User

class Hospital(models.Model):
    name = models.CharField(max_length=255, unique=True)
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=100)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='departments')

    def __str__(self):
        return self.name

class DoctorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    qualifications = models.CharField(max_length=200)
    specializations = models.CharField(max_length=200)  # comma-separated
    experience = models.PositiveIntegerField()

    def __str__(self):
        return self.name

class DoctorAvailability(models.Model):
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    consultation_fee = models.DecimalField(max_digits=8, decimal_places=2)
    def __str__(self):
        return f"{self.doctor.name} - {self.date} {self.start_time} to {self.end_time}"

class PatientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    date_of_birth = models.DateField()
    unique_id = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.name
from django.db import models

class Appointment(models.Model):
    patient = models.ForeignKey('PatientProfile', on_delete=models.CASCADE)
    doctor = models.ForeignKey('DoctorProfile', on_delete=models.CASCADE)
    hospital = models.ForeignKey('Hospital', on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    amount_paid = models.DecimalField(max_digits=8, decimal_places=2)

    doctor_share = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    hospital_share = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"Appointment: {self.patient.name} with {self.doctor.name} on {self.date} at {self.time}"
