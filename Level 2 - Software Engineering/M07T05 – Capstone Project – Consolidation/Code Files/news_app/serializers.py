"""Serializers for API endpoints transforming models to JSON representation."""

from rest_framework import serializers

from .models import Article, Newsletter, Publisher, CustomUser


class ArticleSerializer(serializers.ModelSerializer):
    """Serializer for Article objects."""

    class Meta:
        """Meta options for ArticleSerializer."""

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
    """Serializer for Newsletter objects."""

    class Meta:
        """Meta options for NewsletterSerializer."""

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
    """Serializer for Publisher objects."""

    class Meta:
        """Meta options for PublisherSerializer."""

        model = Publisher
        fields = ['id', 'name', 'created_at']
        read_only_fields = ['id', 'created_at']


class UserSerializer(serializers.ModelSerializer):
    """Serializer for CustomUser objects."""

    class Meta:
        """Meta options for UserSerializer."""

        model = CustomUser
        fields = ['id', 'username', 'role']
