from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
import secrets
from hashlib import sha1
from django.utils import timezone
from django.core.mail import EmailMessage
from django.db import IntegrityError
from django.conf import settings
from .models import ResetToken


def ensure_group(name):
    """Get or create a Django auth group by name."""
    group, _ = Group.objects.get_or_create(name=name)
    return group


def add_permissions_to_user(user, permission_codenames):
    """Attach app-specific permissions to a user when they exist."""
    for codename in permission_codenames:
        try:
            permission = Permission.objects.get(codename=codename, content_type__app_label='eCommerce')
            user.user_permissions.add(permission)
        except Permission.DoesNotExist:
            pass


def login_user(request):
    """Authenticate a user and start a role-aware session."""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            exp_date = datetime(2025, 12, 30)
            now = datetime.now()
            expiry_seconds = int((exp_date - now).total_seconds())
            if expiry_seconds > 0:
                request.session.set_expiry(expiry_seconds)

            request.session['user_id'] = user.id
            request.session['username'] = user.username
            request.session['user_role'] = 'vendor' if user.groups.filter(name='Vendors').exists() else 'buyer'

            return HttpResponseRedirect(reverse('grabsomore:welcome'))
        else:
            return render(request, 'grabsomore/login.html', {'error': 'Invalid credentials'})

    return render(request, 'grabsomore/login.html')


def register_user(request):
    """Register a new buyer or vendor user account."""
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password')
        email = request.POST.get('email', '').strip().lower()
        role = request.POST.get('role', 'buyer')

        if not username or not password or not email:
            return render(request, 'grabsomore/register.html', {'error': 'All fields are required.'})

        if User.objects.filter(email__iexact=email).exists():
            return render(request, 'grabsomore/register.html', {'error': 'That email is already registered.'})

        try:
            user = User.objects.create_user(username=username, password=password, email=email)
        except IntegrityError:
            return render(request, 'grabsomore/register.html', {'error': 'That username is already taken.'})

        if role == 'vendor':
            vendors_group = ensure_group('Vendors')
            user.groups.add(vendors_group)
            add_permissions_to_user(user, ['add_products', 'change_products', 'delete_products', 'view_products'])
        else:
            buyers_group = ensure_group('Buyers')
            user.groups.add(buyers_group)
            add_permissions_to_user(user, ['view_products'])

        add_permissions_to_user(user, ['view_products'])
        user.save()

        login(request, user)
        return redirect(reverse('grabsomore:welcome'))

    return render(request, 'grabsomore/register.html')


def change_user_password(username, new_password):
    """Set a new password for the specified username."""
    user = User.objects.get(username=username)
    user.set_password(new_password)
    user.save()


def logout_user(request):
    """Log out the current user and redirect to login."""
    if request.user is not None:
        logout(request)
    return HttpResponseRedirect(reverse('grabsomore:login'))


@login_required(login_url=reverse_lazy('grabsomore:login'))
def welcome(request):
    """Render the post-login welcome page."""
    return render(request, 'grabsomore/welcome.html')


def build_email(user, reset_url):
    """Build a password reset email message object."""
    subject = 'Password Reset'
    body = f'Hi {user.username},\n\nUse the link below to reset your password:\n{reset_url}\n\nIf you did not request a password reset, you can ignore this message.'
    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'no-reply@authlog.local')
    email = EmailMessage(subject, body, from_email, [user.email])
    return email


def generate_reset_url(request, user):
    """Create and store a time-limited password reset URL."""
    token = secrets.token_urlsafe(24)
    expiry_date = timezone.now() + timedelta(minutes=15)
    hashed_token = sha1(token.encode()).hexdigest()

    ResetToken.objects.create(user=user, token=hashed_token, expiry_date=expiry_date)
    reset_url = reverse('grabsomore:password_reset_form', kwargs={'token': token})
    return request.build_absolute_uri(reset_url)


def send_password_reset(request):
    """Handle password reset requests without revealing account existence."""
    if request.method == 'POST':
        user_email = request.POST.get('email')
        try:
            user = User.objects.get(email=user_email)
            reset_url = generate_reset_url(request, user)
            email = build_email(user, reset_url)
            email.send()
            return render(request, 'grabsomore/reset_email_sent.html', {'email': user_email})
        except User.DoesNotExist:
            return render(request, 'grabsomore/reset_email_sent.html', {'email': user_email})

    return render(request, 'grabsomore/request_password_reset.html')


def reset_user_password(request, token):
    """Validate a reset token and show the reset form."""
    hashed_token = sha1(token.encode()).hexdigest()
    try:
        user_token = ResetToken.objects.get(token=hashed_token, used=False)
        if user_token.expiry_date < timezone.now():
            user_token.delete()
            return render(request, 'grabsomore/password_reset_expired.html')
        return render(request, 'grabsomore/password_reset.html', {'token': token})
    except ResetToken.DoesNotExist:
        return render(request, 'grabsomore/password_reset_invalid.html', {'message': 'The reset link is invalid or expired.'})


def reset_password(request):
    """Validate and apply a new password for a valid reset token."""
    if request.method == 'POST':
        token = request.POST.get('token')
        password = request.POST.get('password')
        password_conf = request.POST.get('password_conf')

        if not all([token, password, password_conf]):
            return render(request, 'grabsomore/password_reset.html', {
                'error': 'Missing fields or invalid reset token.',
                'token': token
            })

        if password != password_conf:
            return render(request, 'grabsomore/password_reset.html', {
                'error': 'Passwords do not match.',
                'token': token
            })

        hashed_token = sha1(token.encode()).hexdigest()
        try:
            reset_token = ResetToken.objects.get(token=hashed_token, used=False)
            if reset_token.expiry_date < timezone.now():
                reset_token.delete()
                return render(request, 'grabsomore/password_reset_expired.html')

            user = reset_token.user
            user.set_password(password)
            user.save()

            reset_token.used = True
            reset_token.save()

            return HttpResponseRedirect(reverse('grabsomore:login'))
        except ResetToken.DoesNotExist:
            return render(request, 'grabsomore/password_reset_invalid.html', {'message': 'The reset token is invalid or has already been used.'})

    return HttpResponseRedirect(reverse('grabsomore:login'))
