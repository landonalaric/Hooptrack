from rest_framework import serializers
from .models import ScoutReport



class ScoutReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScoutReport
        fields = "__all__"
        read_only_fields = ["scout", "academy"]