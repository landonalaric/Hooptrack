from django.db import models
from Teams.models import Team
from academy.models import Academy


class Schedule(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    date_time = models.DateTimeField()
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='schedules')
    academy = models.ForeignKey(Academy, on_delete=models.CASCADE, related_name='schedules')

    def __str__(self):
        return f"{self.title} for {self.team.name} @ {self.date_time}"
