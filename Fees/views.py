from rest_framework import generics, permissions, exceptions

from Fees.serializer import PaymentSerializer


from .models import Payment

from accounts.models import Role, GuardianProfile
from players.models import Player


class GuardianPaymentView(generics.ListCreateAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.role == Role.GUARDIAN:
            try:
                profile = GuardianProfile.objects.get(user=user)
                return Payment.objects.filter(guardian=profile)
            except GuardianProfile.DoesNotExist:
                return Payment.objects.none()

        elif user.role == Role.ADMIN:
            return Payment.objects.filter(player__academy=user.academy)

        return Payment.objects.none()

    def perform_create(self, serializer):
        user = self.request.user

        if user.role != Role.GUARDIAN:
            raise exceptions.PermissionDenied(
                "Only guardians can submit payment receipts."
            )

        try:
            profile = GuardianProfile.objects.get(user=user)
            player = Player.objects.get(
                player_code=profile.player_code,
                academy=user.academy
            )
        except (GuardianProfile.DoesNotExist, Player.DoesNotExist):
            raise exceptions.ValidationError(
                "No active, linked student-athlete matching code."
            )

        serializer.save(
            guardian=profile,
            player=player
        )