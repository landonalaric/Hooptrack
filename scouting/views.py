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

    print("USER:", user)
    print("USER ID:", user.id)
    print("ROLE:", user.role)

    if user.role != Role.SCOUT:
        print("BLOCKED: USER IS NOT A SCOUT")
        raise exceptions.PermissionDenied(
            "Only scouts can log candidate reports."
        )

    try:
        profile = ScoutProfile.objects.get(user=user)
    except ScoutProfile.DoesNotExist:
        print("BLOCKED: SCOUT PROFILE NOT FOUND")
        raise exceptions.ValidationError(
            "Scout profile does not exist for this user."
        )

    print("SCOUT PROFILE:", profile)
    print("SCOUT PROFILE ID:", profile.pk)

    if not profile.academy:
        print("BLOCKED: SCOUT HAS NO ACADEMY")
        raise exceptions.ValidationError(
            "Scout profile is not assigned to an academy."
        )

    print("ACADEMY:", profile.academy)
    print("ACADEMY ID:", profile.academy.pk)

    instance = serializer.save(
        scout=profile,
        academy=profile.academy
    )

    print("=== REPORT SAVED ===")
    print("REPORT ID:", instance.pk)
    print("SCOUT ID:", instance.scout_id)
    print("ACADEMY ID:", instance.academy_id)