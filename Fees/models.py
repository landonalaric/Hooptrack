from django.db import models
from accounts.models import GuardianProfile
from players.models import Player


class Payment(models.Model):
    METHOD_CHOICES = [
        ('MPESA', 'M-Pesa'),
        ('PAYPAL', 'PayPal'),
        ('VISA', 'Visa card'),
        ('MASTERCARD', 'MasterCard'),
        ('KCB', 'KCB bank transfer'),
        ('COOP_BANK', 'Co-operative Bank transfer'),
    ]
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
    ]

    guardian = models.ForeignKey(GuardianProfile, on_delete=models.CASCADE, related_name='card_payments')
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='card_payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=METHOD_CHOICES, default='MPESA')
    receipt_no = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.payment_method} payment of {self.amount} by {self.guardian.fullname} ({self.status})"