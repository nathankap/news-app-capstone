"""REST serializers for news application API resources."""

from rest_framework import serializers

from .models import Article, Newsletter, Publisher, CustomUser


class ArticleSerializer(serializers.ModelSerializer):
    """Serialize article read/write fields for API endpoints."""

    class Meta:
        model = Article
        fields = [
            'id',
            'title',
            'content',
            'author',
            'approved',
            'publisher',
            'created_at']
        read_only_fields = ['id', 'author', 'created_at']


class NewsletterSerializer(serializers.ModelSerializer):
    """Serialize newsletter payloads and linked articles."""

    class Meta:
        model = Newsletter
        fields = [
            'id',
            'title',
            'description',
            'author',
            'created_at',
            'articles']
        read_only_fields = ['id', 'author', 'created_at']


class PublisherSerializer(serializers.ModelSerializer):
    """Serialize publisher records exposed via the API."""

    class Meta:
        model = Publisher
        fields = ['id', 'name', 'created_at']
        read_only_fields = ['id', 'created_at']


class UserSerializer(serializers.ModelSerializer):
    """Serialize minimal user identity and role details."""

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'role']
