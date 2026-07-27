from django.db import models
from django.db import models
from Teams.models import Team
from academy.models import Academy


# Create your models here.

class Player(models.Model):
    fullname = models.CharField(max_length=255)
    age_group = models.CharField(max_length=50, default="Under 14")
    player_code = models.CharField(max_length=50, unique=True)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, related_name='players')
    date_of_birth = models.DateField()
    medical_info = models.TextField(blank=True, null=True)
    contact = models.CharField(max_length=255, help_text="Emergency contact details")
    academy = models.ForeignKey(Academy, on_delete=models.CASCADE, related_name='players')

    def __str__(self):
        return f"{self.fullname} - Code: {self.player_code}"