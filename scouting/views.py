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
            return ScoutReport.objects.filter(
                scout__user=user
            )

        if user.role in [Role.ADMIN, Role.COACH]:
            return ScoutReport.objects.filter(
                academy=user.academy
            )

        return ScoutReport.objects.none()

    def perform_create(self, serializer):
        print("\n========== CREATE REPORT ==========")

        user = self.request.user

        print("USER:", user)
        print("USER ID:", user.id)
        print("ROLE:", user.role)

        # 1. Find ScoutProfile belonging to logged-in user
        profile = ScoutProfile.objects.filter(
            user=user
        ).first()

        print("SCOUT PROFILE:", profile)
        print("SCOUT PROFILE ID:", profile.id if profile else None)

        if profile is None:
            raise exceptions.ValidationError(
                "No ScoutProfile exists for the logged-in user."
            )

        # 2. Find academy
        academy = getattr(user, "academy", None)

        print("ACADEMY:", academy)
        print("ACADEMY ID:", getattr(academy, "id", None))

        if academy is None:
            raise exceptions.ValidationError(
                "The logged-in user has no academy."
            )

        # 3. Get the validated report data
        data = serializer.validated_data

        print("VALIDATED DATA:", data)

        # 4. Explicitly create ScoutReport
        report = ScoutReport.objects.create(
            scout_id=profile.id,
            academy_id=academy.id,
            player_name=data["player_name"],
            age=data["age"],
            potential_overall=data["potential_overall"],
            status=data["status"],
            comments=data["comments"],
            linked_player=data.get("linked_player"),
        )

        print("\n========== REPORT CREATED ==========")
        print("REPORT ID:", report.id)
        print("SCOUT ID:", report.scout_id)
        print("ACADEMY ID:", report.academy_id)
        print("====================================")