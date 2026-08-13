from django.shortcuts import render
from rest_framework import generics, permissions
from django.db.models import Q
from chat.serializer import ChatMessageSerializer, UserSerializer
from .models import ChatMessage
from accounts.models import Role, User


class ChatMessageView(generics.ListCreateAPIView):
    serializer_class = ChatMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return ChatMessage.objects.filter(Q(sender=user) | Q(receiver=user)).order_by('timestamp')

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)


class ChatContactsView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        role_map = {
            Role.ADMIN: [Role.COACH, Role.SCOUT, Role.SUPERADMIN],
            Role.COACH: [Role.ADMIN, Role.GUARDIAN, Role.SCOUT],
            Role.GUARDIAN: [Role.COACH],
            Role.SCOUT: [Role.ADMIN, Role.COACH],
            Role.SUPERADMIN: [Role.ADMIN],
        }
        allowed_roles = role_map.get(self.request.user.role, [])
        return User.objects.filter(role__in=allowed_roles).exclude(id=self.request.user.id)