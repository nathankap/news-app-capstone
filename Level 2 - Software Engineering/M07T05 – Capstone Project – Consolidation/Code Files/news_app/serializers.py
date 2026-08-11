from rest_framework import serializers

from .models import Article, Newsletter, Publisher, CustomUser


class ArticleSerializer(serializers.ModelSerializer):
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
    class Meta:
        model = Publisher
        fields = ['id', 'name', 'created_at']
        read_only_fields = ['id', 'created_at']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'role']
