"""Website and API views for articles and newsletters."""

import requests
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import Article, Newsletter
from .serializers import ArticleSerializer, NewsletterSerializer


def home(request):
    """Render the home page with approved articles and newsletters."""
    articles = Article.objects.filter(
        approved=True).order_by('-created_at')[:5]
    newsletters = Newsletter.objects.order_by('-created_at')[:5]
    return render(request, 'news_app/home.html', {
        'title': 'News App',
        'articles': articles,
        'newsletters': newsletters,
    })


def _notify_approval(article):
    """Notify external log service when an article is approved."""
    try:
        requests.post('http://127.0.0.1:8001/api/approved/', json={
            'article_id': article.id,
            'title': article.title,
        }, timeout=2)
    except requests.RequestException:
        return False
    return True


def approve_article(request, article_id):
    """Allow editors to approve an article and trigger notification."""
    article = get_object_or_404(Article, id=article_id)
    if request.user.is_authenticated and getattr(
            request.user, 'role', None) == 'editor':
        article.approved = True
        article.save()
        _notify_approval(article)
    return redirect('home')


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def article_list_create(request):
    """List approved articles or create a new article for journalists."""
    if request.method == 'GET':
        articles = Article.objects.filter(
            approved=True).order_by('-created_at')
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

    if request.user.role != 'journalist':
        return Response({'detail': 'Only journalists can create articles.'},
                        status=status.HTTP_403_FORBIDDEN)

    serializer = ArticleSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(author=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def article_subscribed(request):
    """Return reader-only feed filtered by current subscriptions."""
    if request.user.role != 'reader':
        articles = Article.objects.filter(
            approved=True).order_by('-created_at')
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

    subscribed_publishers = request.user.subscribed_publishers.values_list(
        'id', flat=True)
    subscribed_journalists = request.user.subscribed_journalists.values_list(
        'id', flat=True)
    q1 = Q(author_id__in=subscribed_journalists)
    q2 = Q(publisher_id__in=subscribed_publishers)
    articles = Article.objects.filter(approved=True).filter(
        q1 | q2
    ).order_by('-created_at')
    serializer = ArticleSerializer(articles, many=True)
    return Response(serializer.data)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def article_detail(request, article_id):
    """Retrieve, update, or delete a single article by role rules."""
    article = get_object_or_404(Article, id=article_id)
    if request.method == 'GET':
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    if request.user.role not in {'journalist', 'editor'}:
        return Response(
            {
                'detail': 'Only journalists and editors can modify articles.'},
            status=status.HTTP_403_FORBIDDEN)

    if request.method == 'PUT':
        serializer = ArticleSerializer(
            article, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    article.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([AllowAny])
def approved_log(request):
    """Receive callback payload for approved article events."""
    return Response({'detail': 'approved article logged',
                     'article_id': request.data.get('article_id')},
                    status=status.HTTP_201_CREATED)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def newsletter_list_create(request):
    """List newsletters or create one for journalist/editor roles."""
    if request.method == 'GET':
        newsletters = Newsletter.objects.all()
        serializer = NewsletterSerializer(newsletters, many=True)
        return Response(serializer.data)

    if request.user.role not in {'journalist', 'editor'}:
        return Response(
            {
                'detail': 'Only journalists and editors'
                'can create newsletters.'},
            status=status.HTTP_403_FORBIDDEN)

    serializer = NewsletterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(author=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
