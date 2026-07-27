from django.shortcuts import render
from rest_framework import viewsets, permissions, exceptions
from players.serializer import PlayerSerializer
from .models import Player
from accounts.models import Role, GuardianProfile

# Create your views here.
class PlayerViewSet(viewsets.ModelViewSet):
    serializer_class = PlayerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == Role.SUPERADMIN:
            return Player.objects.all()
        elif user.role == Role.GUARDIAN:
            try:
                profile = GuardianProfile.objects.get(user=user)
                return Player.objects.filter(player_code=profile.player_code, academy=user.academy)
            except GuardianProfile.DoesNotExist:
                return Player.objects.none()
        return Player.objects.filter(academy=user.academy)

    def perform_create(self, serializer):
        if self.request.user.role not in [Role.ADMIN, Role.COACH]:
            raise exceptions.PermissionDenied("You do not have access to register players.")
        serializer.save(academy=self.request.user.academy)