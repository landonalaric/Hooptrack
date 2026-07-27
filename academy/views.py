from django.shortcuts import render
from rest_framework import viewsets, permissions

from academy.serializer import AcademySerializer
from .models import Academy


# Create your views here.
class AcademyViewSet(viewsets.ModelViewSet):
    queryset = Academy.objects.all()
    serializer_class = AcademySerializer
    permission_classes = [permissions.IsAdminUser]