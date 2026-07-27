

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from academy.models import Academy
from accounts.models import ScoutProfile
from players.models import Player

class ScoutReport(models.Model):
    STATUS_CHOICES = [
        ('PROSPECT', 'Prospect'),
        ('PROVEN', 'Proven'),
    ]
    scout = models.ForeignKey(ScoutProfile, on_delete=models.CASCADE, related_name='reports')
    player_name = models.CharField(max_length=255)
    age = models.IntegerField()
    potential_overall = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(99)],
        help_text="Rating out of 99"
    )
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='PROSPECT')
    comments = models.TextField()
    linked_player = models.ForeignKey(Player, on_delete=models.SET_NULL, null=True, blank=True, related_name='scout_links')
    academy = models.ForeignKey(Academy, on_delete=models.CASCADE, related_name='scout_reports')

    def __str__(self):
        return f"Report: {self.player_name} (Rating: {self.potential_overall}) - {self.status}"
