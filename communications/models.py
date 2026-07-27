from django.db import models
from academy.models import Academy
from accounts.models import User

class Announcement(models.Model):
    academy = models.ForeignKey(Academy, on_delete=models.CASCADE, related_name='announcements')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_announcements')
    title = models.CharField(max_length=255)
    content = models.TextField()
    date_sent = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} sent to {self.academy.name}"

