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

    user = self.request.user

    print("User:", user)
    print("User ID:", user.id)
    print("Role:", getattr(user, "role", None))

    if user.role != Role.SCOUT:
        print("BLOCKED: not a scout")
        raise exceptions.PermissionDenied(
            "Only scouts can log candidate reports."
        )

    try:
        profile = ScoutProfile.objects.get(user=user)

        print("Scout profile:", profile)
        print("Scout profile ID:", profile.id)
        print("Academy:", profile.academy)
        print("Academy ID:", profile.academy.id)

    except ScoutProfile.DoesNotExist:
        print("BLOCKED: no scout profile")

        raise exceptions.ValidationError(
            "Scout profile does not exist for this user."
        )

    instance = serializer.save(
        scout=profile,
        academy=profile.academy
    )

    print("SAVED REPORT:", instance.id)
    print("SCOUT:", instance.scout_id)
    print("ACADEMY:", instance.academy_id)