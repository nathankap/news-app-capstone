from django.contrib.auth.models import AbstractUser, Group
from django.db import models


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('reader', 'Reader'),
        ('editor', 'Editor'),
        ('journalist', 'Journalist'),
    ]
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='reader')
    role_approved = models.BooleanField(default=True)
    subscribed_publishers = models.ManyToManyField(
        'Publisher', blank=True, related_name='subscribers')
    subscribed_journalists = models.ManyToManyField(
        'self', blank=True,
        symmetrical=False,
        related_name='reader_subscribers')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.role == 'journalist':
            self.subscribed_publishers.clear()
            self.subscribed_journalists.clear()
        group_name = self.role.title() if self.role in {
            'reader', 'editor', 'journalist'} else 'Reader'
        group, _ = Group.objects.get_or_create(name=group_name)
        self.groups.set([group])


class Publisher(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    editors = models.ManyToManyField(
        'CustomUser',
        blank=True,
        related_name='managed_publishers')
    journalists = models.ManyToManyField(
        'CustomUser', blank=True, related_name='publisher_journalists')

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='articles')
    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)
    publisher = models.ForeignKey(
        Publisher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True)

    def __str__(self):
        return self.title


class Newsletter(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='newsletters')
    articles = models.ManyToManyField(Article, blank=True)

    def __str__(self):
        return self.title
