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
    print("=== CREATE ATTEMPT ===")
    print("User:", self.request.user, "Role:", getattr(self.request.user, "role", None))

    if self.request.user.role != Role.SCOUT:
        print("BLOCKED: not a scout")
        raise exceptions.PermissionDenied("Only scouts can log candidate reports.")
    try:
        profile = ScoutProfile.objects.get(user=self.request.user)
        print("Scout profile found:", profile, "Academy:", getattr(profile, "academy", "NO ACADEMY FIELD"))
    except ScoutProfile.DoesNotExist:
        print("BLOCKED: no scout profile")
        raise exceptions.ValidationError("Scout profile needs database setup.")

    instance = serializer.save(scout=profile, academy=profile.academy)
    print("SAVED REPORT:", instance.id, instance.player_name)

def get_queryset(self):
    user = self.request.user
    print("=== LIST REQUEST ===")
    print("User:", user, "Role:", getattr(user, "role", None))
    if user.role == Role.SCOUT:
        qs = ScoutReport.objects.filter(scout__user=user)
        print("Scout queryset count:", qs.count(), "IDs:", list(qs.values_list("id", flat=True)))
        return qs
    elif user.role in [Role.ADMIN, Role.COACH]:
        qs = ScoutReport.objects.filter(academy=user.academy)
        print("Admin/coach queryset count:", qs.count())
        return qs
    print("No matching role, returning none()")
    return ScoutReport.objects.none()