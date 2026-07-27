from django.db import models
from academy.models import Academy
from accounts.models import CoachProfile

# Create your models here.
class Team(models.Model):
    name = models.CharField(max_length=100)
    age_group = models.CharField(max_length=50, help_text="e.g. Under 14, Under 17")
    academy = models.ForeignKey(Academy, on_delete=models.CASCADE, related_name='teams')
    coach = models.ForeignKey(CoachProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='teams')

    def __str__(self):
        return f"{self.name} ({self.age_group})"