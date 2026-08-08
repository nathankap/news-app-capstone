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
    group, _ = Group.objects.get_or_create(name=name)
    return group


def add_permissions_to_user(user, permission_codenames):
    for codename in permission_codenames:
        try:
            permission = Permission.objects.get(
                codename=codename, content_type__app_label='eCommerce')
            user.user_permissions.add(permission)
        except Permission.DoesNotExist:
            pass


# This function handles user login
def login_user(request):
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
            request.session['user_role'] = 'vendor' if user.groups.filter(
                name='Vendors').exists() else 'buyer'

            return HttpResponseRedirect(reverse('grabsomore:welcome'))
        else:
            return render(request, 'grabsomore/login.html',
                          {'error': 'Invalid credentials'})

    return render(request, 'grabsomore/login.html')


# This function handles user registration (signing up)
def register_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        role = request.POST.get('role', 'buyer')

        if not username or not password or not email:
            return render(request, 'grabsomore/register.html',
                          {'error': 'All fields are required.'})

        try:
            user = User.objects.create_user(
                username=username, password=password, email=email)
        except IntegrityError:
            return render(request, 'grabsomore/register.html',
                          {'error': 'That username is already taken.'})

        if role == 'vendor':
            vendors_group = ensure_group('Vendors')
            user.groups.add(vendors_group)
            add_permissions_to_user(
                user, [
                    'add_products', 'change_products', 'delete_products', 'view_products'])
        else:
            buyers_group = ensure_group('Buyers')
            user.groups.add(buyers_group)
            add_permissions_to_user(user, ['view_products'])

        add_permissions_to_user(user, ['view_products'])
        user.save()

        login(request, user)
        return redirect(reverse('grabsomore:welcome'))

    return render(request, 'grabsomore/register.html')


# Helper function to change a user's password securely
def change_user_password(username, new_password):
    user = User.objects.get(username=username)
    user.set_password(new_password)
    user.save()


# Logs the user out and redirects to login page
def logout_user(request):
    if request.user is not None:
        logout(request)
    return HttpResponseRedirect(reverse('grabsomore:login'))


# Only logged-in users can see the welcome page
@login_required(login_url=reverse_lazy('grabsomore:login'))
def welcome(request):
    return render(request, 'grabsomore/welcome.html')


# Creates the email object to send for password reset
def build_email(user, reset_url):
    subject = 'Password Reset'
    body = f'Hi {user.username},\n\nUse the link below to reset your password:\n{reset_url}\n\nIf you did not request a password reset, you can ignore this message.'
    from_email = getattr(
        settings,
        'DEFAULT_FROM_EMAIL',
        'no-reply@authlog.local')
    email = EmailMessage(subject, body, from_email, [user.email])
    return email


# Creates a secure reset URL with a token that expires in 15 minutes
def generate_reset_url(request, user):
    token = secrets.token_urlsafe(24)
    expiry_date = timezone.now() + timedelta(minutes=15)
    hashed_token = sha1(token.encode()).hexdigest()

    ResetToken.objects.create(
        user=user,
        token=hashed_token,
        expiry_date=expiry_date)
    reset_url = reverse(
        'grabsomore:password_reset_form',
        kwargs={
            'token': token})
    return request.build_absolute_uri(reset_url)


# Handles sending the password reset email after user submits their email
def send_password_reset(request):
    if request.method == 'POST':
        user_email = request.POST.get('email')
        try:
            user = User.objects.get(email=user_email)
            reset_url = generate_reset_url(request, user)
            email = build_email(user, reset_url)
            email.send()
            return render(request,
                          'grabsomore/reset_email_sent.html',
                          {'email': user_email})
        except User.DoesNotExist:
            return render(request,
                          'grabsomore/reset_email_sent.html',
                          {'email': user_email})

    return render(request, 'grabsomore/request_password_reset.html')


# This view is called when user clicks the reset link in their email
def reset_user_password(request, token):
    hashed_token = sha1(token.encode()).hexdigest()
    try:
        user_token = ResetToken.objects.get(token=hashed_token, used=False)
        if user_token.expiry_date < timezone.now():
            user_token.delete()
            return render(request, 'grabsomore/password_reset_expired.html')
        return render(request,
                      'grabsomore/password_reset.html',
                      {'token': token})
    except ResetToken.DoesNotExist:
        return render(request,
                      'grabsomore/password_reset_invalid.html',
                      {'message': 'The reset link is invalid or expired.'})


# Handles the password reset form submission (when user enters new password)
def reset_password(request):
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
            reset_token = ResetToken.objects.get(
                token=hashed_token, used=False)
            if reset_token.expiry_date < timezone.now():
                reset_token.delete()
                return render(
                    request, 'grabsomore/password_reset_expired.html')

            user = reset_token.user
            user.set_password(password)
            user.save()

            reset_token.used = True
            reset_token.save()

            return HttpResponseRedirect(reverse('grabsomore:login'))
        except ResetToken.DoesNotExist:
            return render(request, 'grabsomore/password_reset_invalid.html',
                          {'message': 'The reset token is invalid or has already been used.'})

    return HttpResponseRedirect(reverse('grabsomore:login'))
