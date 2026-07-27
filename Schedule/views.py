from django.shortcuts import render
from rest_framework import viewsets, permissions
from Schedule.serializer import ScheduleSerializer
from .models import Schedule
from accounts.models import Role

class ScheduleViewSet(viewsets.ModelViewSet):
    serializer_class = ScheduleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == Role.SUPERADMIN:
            return Schedule.objects.all()
        return Schedule.objects.filter(academy=user.academy)

    def perform_create(self, serializer):
        serializer.save(academy=self.request.user.academy)

