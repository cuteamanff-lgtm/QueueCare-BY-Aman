from django.db import models
from django.utils import timezone

class Token(models.Model):
    STATUS_CHOICES = [
        ("WAITING", "Waiting"), ("SERVING", "Serving"),
        ("COMPLETED", "Completed"), ("SKIPPED", "Skipped"),
        ("CANCELLED", "Cancelled"),
    ]
    token_number = models.CharField(max_length=12, unique=True)
    full_name = models.CharField(max_length=120)
    mobile_number = models.CharField(max_length=10)
    service = models.CharField(max_length=120)
    priority = models.BooleanField(default=False)
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default="WAITING")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-priority", "created_at"]

    def __str__(self):
        return f"{self.token_number} — {self.full_name}"
