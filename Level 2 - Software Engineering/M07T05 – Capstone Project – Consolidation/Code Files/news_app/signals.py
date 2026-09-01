"""Signal receivers for automatic group and permission creation."""

from django.contrib.auth.models import Group, Permission
from django.db.models.signals import post_migrate
from django.dispatch import receiver


@receiver(post_migrate)
def create_groups_and_permissions(sender, **kwargs):
    """Create default user roles and assign permissions after migrations."""
    if sender.name != 'news_app':
        return

    roles = {
        'Reader': [
            'view_article',
            'view_newsletter'],
        'Editor': [
            'view_article',
            'view_newsletter',
            'change_article',
            'delete_article',
            'change_newsletter',
            'delete_newsletter'],
        'Journalist': [
            'add_article',
            'view_article',
            'change_article',
            'delete_article',
            'add_newsletter',
            'view_newsletter',
            'change_newsletter',
            'delete_newsletter'],
    }

    for group_name, permission_codes in roles.items():
        group, _ = Group.objects.get_or_create(name=group_name)
        permissions = Permission.objects.filter(codename__in=permission_codes)
        group.permissions.set(permissions)
