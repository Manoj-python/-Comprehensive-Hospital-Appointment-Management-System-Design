from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RegisterDoctorView, RegisterPatientView, LoginView,
    HospitalViewSet, DepartmentViewSet, DoctorProfileViewSet,
    DoctorAvailabilityViewSet, PatientProfileViewSet, AppointmentViewSet,
    doctor_me, patient_me,
    AdminAppointmentViewSet, AdminDoctorViewSet,
    AdminPatientViewSet, AdminHospitalViewSet,
    AdminLoginView, AdminDashboardData
)

# ✅ Main Router (for normal users)
router = DefaultRouter()
router.register('hospitals', HospitalViewSet)
router.register('departments', DepartmentViewSet)
router.register('doctors', DoctorProfileViewSet)
router.register('availabilities', DoctorAvailabilityViewSet)
router.register('patients', PatientProfileViewSet)
router.register('appointments', AppointmentViewSet)

# ✅ Admin Router (only for staff/admin)
admin_router = DefaultRouter()
admin_router.register('admin/appointments', AdminAppointmentViewSet, basename='admin-appointments')
admin_router.register('admin/doctors', AdminDoctorViewSet, basename='admin-doctors')
admin_router.register('admin/patients', AdminPatientViewSet, basename='admin-patients')
admin_router.register('admin/hospitals', AdminHospitalViewSet, basename='admin-hospitals')

# ✅ Final URL patterns
urlpatterns = [
    # 🔐 Auth endpoints
    path('register/doctor/', RegisterDoctorView.as_view(), name='register-doctor'),
    path('register/patient/', RegisterPatientView.as_view(), name='register-patient'),
    path('login/', LoginView.as_view(), name='user-login'),

    # 👤 Profile endpoints
    path('doctors/me/', doctor_me, name='doctor-me'),
    path('patients/me/', patient_me, name='patient-me'),

    # 📦 Include Routers
    path('', include(router.urls)),         # Normal CRUD endpoints
    path('', include(admin_router.urls)),   # Admin-read-only endpoints

    # 🛡️ Admin-specific
    path('admin/login/', AdminLoginView.as_view(), name='admin-login'),
    path('admin/data/', AdminDashboardData.as_view(), name='admin-dashboard-data'),
]
