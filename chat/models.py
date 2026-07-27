from django.db import models
from django.db import models
from django.core.exceptions import ValidationError
from accounts.models import User, Role

class ChatMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def clean(self):
        s_role, r_role = self.sender.role, self.receiver.role
        allowed_pairs = [
            (Role.ADMIN, Role.COACH), (Role.COACH, Role.ADMIN),
            (Role.COACH, Role.GUARDIAN), (Role.GUARDIAN, Role.COACH),
            (Role.ADMIN, Role.SCOUT), (Role.SCOUT, Role.ADMIN),
            (Role.SCOUT, Role.COACH), (Role.COACH, Role.SCOUT)
        ]
        if (s_role, r_role) not in allowed_pairs:
            raise ValidationError(f"Direct messaging is blocked between roles: {s_role} and {r_role}")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"From {self.sender.username} to {self.receiver.username} at {self.timestamp}"

