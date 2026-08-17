from rest_framework import serializers
from .models import Schedule
from Teams.models import Team

class ScheduleSerializer(serializers.ModelSerializer):
    team = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Team.objects.all()
    )

    class Meta:
        model = Schedule
        fields = '__all__'
        read_only_fields = ['academy']