"""Django admin site registrations for CustomUser, Publisher, Article, and Newsletter models."""

from django.contrib import admin

from .models import Article, CustomUser, Newsletter, Publisher


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    """Admin configuration for CustomUser model."""

    list_display = ('username', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    """Admin configuration for Publisher model."""

    list_display = ('name', 'created_at')


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    """Admin configuration for Article model."""

    list_display = ('title', 'author', 'publisher', 'approved', 'created_at')
    list_filter = ('approved', 'publisher')
    search_fields = ('title', 'content')


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    """Admin configuration for Newsletter model."""

    list_display = ('title', 'author', 'created_at')
    search_fields = ('title', 'description')
