from rest_framework import serializers
from .models import Payment



class PaymentSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    class Meta:
        model = Payment
        fields = "__all__"
        read_only_fields = ("guardian", "player", "date", "verified_by_admin")

    def get_status(self, obj):
        return "COMPLETED" if obj.verified_by_admin else "PENDING"