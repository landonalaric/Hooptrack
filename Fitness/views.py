from rest_framework import viewsets, permissions, exceptions

from Fitness.serializer import FitnessLogSerializer
from .models import FitnessLog

from accounts.models import Role, GuardianProfile


class FitnessLogViewSet(viewsets.ModelViewSet):
    serializer_class = FitnessLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.role == Role.SUPERADMIN:
            return FitnessLog.objects.all()

        if user.role == Role.GUARDIAN:
            try:
                profile = GuardianProfile.objects.get(
                    user=user
                )

                return FitnessLog.objects.filter(
                    player__player_code=profile.player_code,
                    player__academy=user.academy
                )

            except GuardianProfile.DoesNotExist:
                return FitnessLog.objects.none()

        return FitnessLog.objects.filter(
            player__academy=user.academy
        )

    def perform_create(self, serializer):
        if self.request.user.role not in [
            Role.ADMIN,
            Role.COACH
        ]:
            raise exceptions.PermissionDenied(
                "Only coaches and admins can register fitness and injury reports."
            )

        serializer.save()
