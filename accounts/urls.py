from django.urls import path
from .views import CustomLoginView, AcademyRegistrationView, AdminCreateUserView, ScoutIndependentSignupView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='auth-login'),
    path('superadmin/register-academy/', AcademyRegistrationView.as_view(), ),
    path('admin/create-user/', AdminCreateUserView.as_view(), ),
    path('scout/signup/', ScoutIndependentSignupView.as_view(), ),
]