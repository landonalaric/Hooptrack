from django.shortcuts import render
from rest_framework import viewsets, permissions, exceptions

from Teams.serializer import TeamSerializer
from .models import Team

from accounts.models import Role
# Create your views here.
class TeamViewSet(viewsets.ModelViewSet):
    serializer_class = TeamSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == Role.SUPERADMIN:
            return Team.objects.all()
        return Team.objects.filter(academy=user.academy)

    def perform_create(self, serializer):
        if self.request.user.role != Role.ADMIN:
            raise exceptions.PermissionDenied("Only academy admins can create teams.")
        serializer.save(academy=self.request.user.academy)