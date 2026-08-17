from rest_framework import serializers
from .models import FitnessLog


class FitnessLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = FitnessLog
        fields = "__all__"
        read_only_fields = ["logged_date"]