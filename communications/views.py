from django.shortcuts import render
from rest_framework import viewsets, permissions, exceptions
from communications.serializer import AnnouncementSerializer
from .models import Announcement
from accounts.models import Role

class AnnouncementViewSet(viewsets.ModelViewSet):
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer

    def perform_create(self, serializer):
        serializer.save(
            sender=self.request.user,
            academy=self.request.user.academy,  # adjust to however academy is resolved for this user
        )
    
def perform_create(self, serializer):
    if self.request.user.role not in [Role.ADMIN, Role.COACH]:
        raise exceptions.PermissionDenied("Only coaches and admins can release global academy announcements.")
    if not self.request.user.academy:
        raise exceptions.ValidationError("Your account is not linked to an academy.")
    serializer.save(sender=self.request.user, academy=self.request.user.academy)

