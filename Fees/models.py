from django.db import models
from accounts.models import GuardianProfile
from players.models import Player

class Payment(models.Model):
    guardian = models.ForeignKey(GuardianProfile, on_delete=models.CASCADE, related_name='payments')
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, default="M-Pesa Screenshot Upload")
    date = models.DateTimeField(auto_now_add=True)
    receipt_no = models.CharField(max_length=100, unique=True)
    verified_by_admin = models.BooleanField(default=False)

    def __str__(self):
        return f"Payment of {self.amount} by {self.guardian.fullname} for {self.player.fullname}"