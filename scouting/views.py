from django.shortcuts import render
from rest_framework import viewsets, permissions, exceptions
from scouting.serializer import ScoutReportSerializer
from .models import ScoutReport
from accounts.models import Role, ScoutProfile

class ScoutReportViewSet(viewsets.ModelViewSet):
    serializer_class = ScoutReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == Role.SCOUT:
            return ScoutReport.objects.filter(scout__user=user)
        elif user.role in [Role.ADMIN, Role.COACH]:
            return ScoutReport.objects.filter(academy=user.academy)
        return ScoutReport.objects.none()

    def perform_create(self, serializer):
        if self.request.user.role != Role.SCOUT:
            raise exceptions.PermissionDenied("Only scouts can log candidate reports.")
        try:
            profile = ScoutProfile.objects.get(user=self.request.user)
        except ScoutProfile.DoesNotExist:
            raise exceptions.ValidationError("Scout profile needs database setup.")

        serializer.save(scout=profile, academy=profile.academy)