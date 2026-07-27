from django.db import models
from django.db import models
from Schedule.models import Schedule
from players.models import Player


# Create your models here.
class Attendance(models.Model):
    STATUS_CHOICES = [
        ('PRESENT', 'Present'),
        ('ABSENT', 'Absent'),
        ('EXCUSED', 'Excused'),
    ]
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='attendances')
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name='attendance_records')
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PRESENT')

    class Meta:
        unique_together = ('player', 'schedule')

    def __str__(self):
        return f"{self.player.fullname} - {self.schedule.title}: {self.status}"