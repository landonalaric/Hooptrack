
from django.db import models
from players.models import Player
# Create your models here.
class FitnessLog(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='fitness_logs')
    logged_date = models.DateField(auto_now_add=True)
    fitness_status = models.TextField(default="Excellent condition")
    injury_status = models.TextField(default="Healthy / No Injuries")
    weight_kg = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    height_cm = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"Fitness Log: {self.player.fullname} on {self.logged_date}"