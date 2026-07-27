from django.shortcuts import render
from rest_framework import viewsets, permissions
from Attendance.serializer import AttendanceSerializer
from .models import Attendance

from accounts.models import Role, GuardianProfile
# Create your views here.
class AttendanceViewSet(viewsets.ModelViewSet):
    serializer_class = AttendanceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == Role.SUPERADMIN:
            return Attendance.objects.all()
        elif user.role == Role.GUARDIAN:
            try:
                profile = GuardianProfile.objects.get(user=user)
                return Attendance.objects.filter(player__player_code=profile.player_code, player__academy=user.academy)
            except GuardianProfile.DoesNotExist:
                return Attendance.objects.none()
        return Attendance.objects.filter(player__academy=user.academy)