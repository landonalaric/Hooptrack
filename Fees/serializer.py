from rest_framework import serializers
from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            'id', 'guardian', 'player', 'amount', 'payment_method',
            'receipt_no', 'status', 'date',
        ]
        read_only_fields = ['guardian', 'player', 'status', 'date']


class PaymentStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'status']