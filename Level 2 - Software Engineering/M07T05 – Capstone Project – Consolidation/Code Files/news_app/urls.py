"""URL pattern routing definitions for news_app views and API endpoints."""

from django.urls import path
from . import views

urlpatterns = [
    path(
        '',
        views.home,
        name='home'),
    path(
        'approve-article/<int:article_id>/',
        views.approve_article,
        name='approve_article'),
    path(
        'api/approved/',
        views.approved_log,
        name='approved_log'),
    path(
        'api/articles/subscribed/',
        views.article_subscribed,
        name='article_subscribed'),
    path(
        'api/articles/<int:article_id>/',
        views.article_detail,
        name='article_detail'),
    path(
        'api/articles/',
        views.article_list_create,
        name='article_list_create'),
    path(
        'api/newsletters/',
        views.newsletter_list_create,
        name='newsletter_list_create'),
]
