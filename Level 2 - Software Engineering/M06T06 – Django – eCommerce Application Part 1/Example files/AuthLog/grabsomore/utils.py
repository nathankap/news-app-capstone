from django.core.mail import EmailMessage  # Used to create and send emails
from hashlib import sha1  # Used to securely hash data (like tokens)
from datetime import datetime, timedelta  # To handle dates and times
from .models import ResetToken  # Our model to store password reset tokens
from django.urls import reverse  # To get URL from named paths


def generate_reset_url(user):
    """Generate and persist a reset token URL for the provided user."""

    token = sha1((user.username + str(datetime.now())).encode()).hexdigest()

    expiry = datetime.now() + timedelta(hours=1)

    ResetToken.objects.create(user=user, token=token, expiry_date=expiry)

    return reverse('grabsomore:password_reset_token', kwargs={'token': token})


def build_email(user, url):
    """Build a password reset email message for the user."""

    subject = 'Password Reset Request'  # Email subject line

    body = f'Hello {user.username},\n\nClick the link below to reset your password:\n\nhttp://localhost:8000{url}'

    email = EmailMessage(subject, body, to=[user.email])

    return email
