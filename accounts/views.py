from django.shortcuts import render
from django.contrib.auth.base_user import BaseUserManager
from rest_framework import viewsets, permissions, status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.exceptions import ValidationError

from academy.serializer import AcademySerializer
from accounts.serializer import UserSerializer
from academy.models import Academy

from .models import User, Role, AdminProfile, CoachProfile, GuardianProfile, ScoutProfile


class CustomUserManager(BaseUserManager):

    def create_user(self, username, email, password=None, role=None, **extra_fields):

        if not email:
            raise ValueError("The Email field must be set")

        email = self.normalize_email(email)

        user = self.model(
            username=username,
            email=email,
            role=role,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)

        return user


    def create_superuser(self, username, email, password=None, **extra_fields):

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(
            username=username,
            email=email,
            password=password,
            role=Role.SUPERADMIN,
            **extra_fields
        )


# Create your views here.
class CustomLoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        coach_id = request.data.get('coach_id')
        player_code = request.data.get('player_code')

        if not username or not password:
            return Response({"error": "Username and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"error": "Invalid login credentials."}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.check_password(password):
            return Response({"error": "Invalid login credentials."}, status=status.HTTP_401_UNAUTHORIZED)

        if user.role == Role.COACH:
            if not coach_id:
                return Response({"error": "Coach ID is required for Coach login."}, status=status.HTTP_400_BAD_REQUEST)
            try:
                coach_profile = CoachProfile.objects.get(user=user)
                if coach_profile.coach_id != coach_id:
                    return Response({"error": "Invalid Coach ID."}, status=status.HTTP_401_UNAUTHORIZED)
            except CoachProfile.DoesNotExist:
                return Response({"error": "Coach profile not initialized."}, status=status.HTTP_400_BAD_REQUEST)

        elif user.role == Role.GUARDIAN:
            if not player_code:
                return Response({"error": "Player code is required for Guardian login."}, status=status.HTTP_400_BAD_REQUEST)
            try:
                guardian_profile = GuardianProfile.objects.get(user=user)
                if guardian_profile.player_code != player_code:
                    return Response({"error": "Invalid player code."}, status=status.HTTP_412_PRECONDITION_FAILED)
            except GuardianProfile.DoesNotExist:
                return Response({"error": "Guardian profile not initialized."}, status=status.HTTP_400_BAD_REQUEST)

        refresh = RefreshToken.for_user(user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user_id": user.pk,
            "role": user.role,
            "username": user.username,
            "academy": user.academy.id if user.academy else None
        }, status=status.HTTP_200_OK)


class AcademyRegistrationView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        if request.user.role != Role.SUPERADMIN:
            return Response({"error": "Only superadmins can create Academies and Admins."}, status=status.HTTP_403_FORBIDDEN)

        academy_name = request.data.get('academy_name')
        location = request.data.get('location')
        admin_username = request.data.get('admin_username')
        admin_email = request.data.get('admin_email')
        admin_password = request.data.get('admin_password')
        admin_fullname = request.data.get('admin_fullname')
        admin_phone = request.data.get('admin_phone_number')

        if not all([academy_name, location, admin_username, admin_email, admin_password, admin_fullname]):
            return Response({"error": "Missing parameters for academy registration."}, status=status.HTTP_400_BAD_REQUEST)

        academy = Academy.objects.create(name=academy_name, location=location)

        admin_user = User.objects.create_user(
            username=admin_username,
            email=admin_email,
            password=admin_password,
            role=Role.ADMIN,
            phone_number=admin_phone,
            academy=academy
        )
        AdminProfile.objects.create(user=admin_user, fullname=admin_fullname)

        return Response({
            "message": "Academy and Academy Admin successfully registered.",
            "academy": AcademySerializer(academy).data,
            "admin": UserSerializer(admin_user).data
        }, status=status.HTTP_201_CREATED)


class AdminCreateUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        if request.user.role != Role.ADMIN:
            return Response({"error": "Only Academy Admins can create profiles."}, status=status.HTTP_403_FORBIDDEN)

        target_role = request.data.get('role')
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        fullname = request.data.get('fullname')
        phone_number = request.data.get('phone_number')

        if not all([target_role, username, email, password, fullname]):
            return Response({"error": "Missing critical fields for account setup."}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            role=target_role,
            phone_number=phone_number,
            academy=request.user.academy
        )

        if target_role == Role.ADMIN:
            AdminProfile.objects.create(user=user, fullname=fullname)
        elif target_role == Role.COACH:
            coach_id = request.data.get('coach_id')
            if not coach_id:
                user.delete()
                return Response({"error": "coach_id is required."}, status=status.HTTP_400_BAD_REQUEST)
            CoachProfile.objects.create(user=user, fullname=fullname, coach_id=coach_id)
        elif target_role == Role.GUARDIAN:
            player_code = request.data.get('player_code')
            if not player_code:
                user.delete()
                return Response({"error": "player_code is required."}, status=status.HTTP_400_BAD_REQUEST)
            GuardianProfile.objects.create(user=user, fullname=fullname, player_code=player_code)
        elif target_role == Role.SCOUT:
            region = request.data.get('region', 'Global')
            ScoutProfile.objects.create(user=user, fullname=fullname, region=region)
        else:
            user.delete()
            return Response({"error": "Invalid role specified."}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": f"{target_role} profile successfully initialized."}, status=status.HTTP_201_CREATED)


class ScoutIndependentSignupView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        fullname = request.data.get('fullname')
        phone_number = request.data.get('phone_number')
        region = request.data.get('region', 'Global')

        if not all([username, email, password, fullname]):
            return Response({"error": "Missing input registration details."}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            role=Role.SCOUT,
            phone_number=phone_number
        )
        ScoutProfile.objects.create(user=user, fullname=fullname, region=region)

        return Response({"message": "Scout successfully registered."}, status=status.HTTP_201_CREATED)