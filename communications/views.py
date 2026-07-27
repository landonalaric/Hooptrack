from django.shortcuts import render
from rest_framework import viewsets, permissions, exceptions
from communications.serializer import AnnouncementSerializer
from .models import Announcement
from accounts.models import Role

class AnnouncementViewSet(viewsets.ModelViewSet):
    serializer_class = AnnouncementSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Announcement.objects.filter(academy=user.academy).order_by('-date_sent')

    def perform_create(self, serializer):
        if self.request.user.role not in [Role.ADMIN, Role.COACH]:
            raise exceptions.PermissionDenied("Only coaches and admins can release global academy announcements.")
        serializer.save(sender=self.request.user, academy=self.request.user.academy)

