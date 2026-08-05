from rest_framework import serializers
from .models import Announcement

class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = ["id", "title", "content", "date_sent", "academy", "sender"]
        read_only_fields = ["academy", "sender", "date_sent"]