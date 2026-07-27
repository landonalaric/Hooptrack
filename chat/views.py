from django.shortcuts import render
from rest_framework import generics, permissions
from django.db.models import Q
from chat.serializer import ChatMessageSerializer
from .models import ChatMessage


class ChatMessageView(generics.ListCreateAPIView):
    serializer_class = ChatMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return ChatMessage.objects.filter(Q(sender=user) | Q(receiver=user)).order_by('timestamp')

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

