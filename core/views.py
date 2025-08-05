from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authtoken.models import Token
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from .models import (
    Hospital,
    Department,
    DoctorProfile,
    DoctorAvailability,
    PatientProfile,
    Appointment
)
from .serializers import (
    HospitalSerializer,
    DepartmentSerializer,
    DoctorProfileSerializer,
    DoctorAvailabilitySerializer,
    PatientProfileSerializer,
    AppointmentSerializer
)

# ----------------- Authenticated Profile Views -----------------

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def doctor_me(request):
    try:
        doctor = DoctorProfile.objects.get(user=request.user)
        serializer = DoctorProfileSerializer(doctor)
        return Response(serializer.data)
    except DoctorProfile.DoesNotExist:
        return Response({'detail': 'Doctor not found'}, status=404)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def patient_me(request):
    try:
        patient = PatientProfile.objects.get(user=request.user)
        serializer = PatientProfileSerializer(patient)
        return Response(serializer.data)
    except PatientProfile.DoesNotExist:
        return Response({'detail': 'Patient not found'}, status=404)

# views.py (start of file)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .models import DoctorProfile, PatientProfile

class RegisterDoctorView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        user = User.objects.create_user(username=data['username'], password=data['password'])
        DoctorProfile.objects.create(
            user=user,
            name=data['name'],
            qualifications=data['qualifications'],
            specializations=data['specializations'],
            experience=data['experience']
        )
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_201_CREATED)

class RegisterPatientView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        user = User.objects.create_user(username=data['username'], password=data['password'])
        PatientProfile.objects.create(
            user=user,
            name=data['name'],
            gender=data['gender'],
            date_of_birth=data['date_of_birth'],
            unique_id=data['unique_id']
        )
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    def post(self, request):
        user = authenticate(username=request.data['username'], password=request.data['password'])
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        return Response({'error': 'Invalid credentials'}, status=400)

# ----------------- ViewSets -----------------

class HospitalViewSet(viewsets.ModelViewSet):
    queryset = Hospital.objects.all()
    serializer_class = HospitalSerializer

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

class DoctorProfileViewSet(viewsets.ModelViewSet):
    queryset = DoctorProfile.objects.all()
    serializer_class = DoctorProfileSerializer

class DoctorAvailabilityViewSet(viewsets.ModelViewSet):
    queryset = DoctorAvailability.objects.all()
    serializer_class = DoctorAvailabilitySerializer

class PatientProfileViewSet(viewsets.ModelViewSet):
    queryset = PatientProfile.objects.all()
    serializer_class = PatientProfileSerializer
from rest_framework.response import Response
from rest_framework import status

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

    def create(self, request, *args, **kwargs):
        try:
            print("📩 Incoming request data:", request.data)
            return super().create(request, *args, **kwargs)
        except Exception as e:
            import traceback
            traceback.print_exc()  # 👈 will show the full error in your terminal
            return Response({'error': str(e)}, status=500)


# ----------------- Admin Read-Only ViewSets -----------------

class AdminAppointmentViewSet(ReadOnlyModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAdminUser]

class AdminDoctorViewSet(ReadOnlyModelViewSet):
    queryset = DoctorProfile.objects.all()
    serializer_class = DoctorProfileSerializer
    permission_classes = [IsAdminUser]

class AdminPatientViewSet(ReadOnlyModelViewSet):
    queryset = PatientProfile.objects.all()
    serializer_class = PatientProfileSerializer
    permission_classes = [IsAdminUser]

class AdminHospitalViewSet(ReadOnlyModelViewSet):
    queryset = Hospital.objects.all()
    serializer_class = HospitalSerializer
    permission_classes = [IsAdminUser]

# ----------------- Admin Login -----------------

class AdminLoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)

        if user and user.is_staff:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'is_staff': user.is_staff
                }
            })
        return Response({'detail': 'Invalid admin credentials or not an admin.'}, status=status.HTTP_401_UNAUTHORIZED)

# ----------------- Admin Dashboard -----------------

class AdminDashboardData(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not request.user.is_staff:
            return Response({"detail": "Access denied"}, status=403)

        data = []
        total_earnings = 0
        total_doctor_earnings = 0
        total_hospital_earnings = 0

        for hospital in Hospital.objects.all():
            hospital_appointments = Appointment.objects.filter(hospital=hospital)
            hospital_doctors = DoctorProfile.objects.filter(
                id__in=hospital_appointments.values_list('doctor_id', flat=True).distinct()
            )

            hospital_earning = sum(appt.hospital_share or 0 for appt in hospital_appointments)
            doctor_earning = sum(appt.doctor_share or 0 for appt in hospital_appointments)
            total = sum(appt.amount_paid for appt in hospital_appointments)

            total_earnings += total
            total_doctor_earnings += doctor_earning
            total_hospital_earnings += hospital_earning

            doctors_data = []
            for doc in hospital_doctors:
                doc_appts = hospital_appointments.filter(doctor=doc)
                doc_earning = sum(a.doctor_share or 0 for a in doc_appts)

                doctors_data.append({
                    "id": doc.id,
                    "name": doc.name,
                    "qualifications": doc.qualifications,
                    "specializations": doc.specializations,
                    "experience": doc.experience,
                    "total_appointments": doc_appts.count(),
                    "earnings": doc_earning,
                    "appointments": [
                        {
                            "patient_name": appt.patient.name,
                            "date": appt.date,
                            "time": appt.time,
                            "amount_paid": appt.amount_paid,
                            "doctor_share": appt.doctor_share,
                            "hospital_share": appt.hospital_share
                        }
                        for appt in doc_appts
                    ]
                })

            data.append({
                "hospital_id": hospital.id,
                "hospital_name": hospital.name,
                "location": hospital.location,
                "total_appointments": hospital_appointments.count(),
                "total_earnings": total,
                "hospital_earnings": hospital_earning,
                "doctor_earnings": doctor_earning,
                "doctors": doctors_data
            })

        all_patients = list(PatientProfile.objects.values("id", "name", "gender", "date_of_birth", "unique_id"))

        return Response({
            "total_system_earnings": total_earnings,
            "total_doctor_earnings": total_doctor_earnings,
            "total_hospital_earnings": total_hospital_earnings,
            "hospitals": data,
            "patients": all_patients
        })
