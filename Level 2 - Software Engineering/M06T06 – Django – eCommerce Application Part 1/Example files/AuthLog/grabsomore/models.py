from django.db import models
from django.conf import settings

class ResetToken(models.Model):
    """Stores a one-time password reset token for a user."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    token = models.CharField(max_length=255, unique=True)
    expiry_date = models.DateTimeField()
    used = models.BooleanField(default=False)

    def __str__(self):
        """Return a compact reset token description for debugging."""
        return f"ResetToken(user={self.user.username}, token={self.token[:10]}..., used={self.used})"
