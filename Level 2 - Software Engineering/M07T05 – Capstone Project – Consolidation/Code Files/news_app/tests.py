"""Core API and workflow tests for the news application."""

from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from .models import Article, Newsletter, Publisher


class NewsApiTests(TestCase):
    """Verify article/newsletter endpoints and role permissions."""

    def setUp(self):
        """Create users and seed article/newsletter test data."""
        self.client = APIClient()
        self.user_model = get_user_model()
        self.reader = self.user_model.objects.create_user(
            username='reader', password='secret', role='reader')
        self.journalist = self.user_model.objects.create_user(
            username='journalist', password='secret', role='journalist')
        self.editor = self.user_model.objects.create_user(
            username='editor', password='secret', role='editor')
        self.publisher = Publisher.objects.create(name='Test Publisher')
        self.article = Article.objects.create(
            title='Example',
            content='Body',
            author=self.journalist,
            publisher=self.publisher,
            approved=True,
        )
        self.newsletter = Newsletter.objects.create(
            title='Weekly', description='desc', author=self.journalist)
        self.newsletter.articles.add(self.article)

    def test_home_page_lists_approved_articles_and_newsletters(self):
        """Home page should render approved article and newsletter content."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Example')
        self.assertContains(response, 'Weekly')

    def test_reader_can_list_approved_articles(self):
        """Readers can fetch the approved article list endpoint."""
        self.client.force_authenticate(self.reader)
        response = self.client.get('/api/articles/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_journalist_can_create_article(self):
        """Journalists can create a new article through the API."""
        self.client.force_authenticate(self.journalist)
        response = self.client.post('/api/articles/', {
            'title': 'New',
            'content': 'Content',
            'publisher': self.publisher.id,
        }, format='json')
        self.assertEqual(response.status_code, 201)

    def test_reader_can_list_only_subscribed_articles(self):
        """Subscribed feed should return only matched publisher/journalist content."""
        other_publisher = Publisher.objects.create(name='Other Publisher')
        other_article = Article.objects.create(
            title='Other',
            content='Body',
            author=self.journalist,
            publisher=other_publisher,
            approved=True)
        self.reader.subscribed_publishers.add(self.publisher)
        self.client.force_authenticate(self.reader)
        response = self.client.get('/api/articles/subscribed/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]['title'], 'Example')
        self.assertNotEqual(response.json()[0]['title'], other_article.title)

    def test_journalist_can_update_article(self):
        """Journalists can update an existing article they own."""
        self.client.force_authenticate(self.journalist)
        response = self.client.put(
            f'/api/articles/{self.article.id}/',
            {'title': 'Updated'},
            format='json')
        self.assertEqual(response.status_code, 200)
        self.article.refresh_from_db()
        self.assertEqual(self.article.title, 'Updated')

    def test_editor_can_delete_article(self):
        """Editors can delete articles through the API."""
        self.client.force_authenticate(self.editor)
        response = self.client.delete(f'/api/articles/{self.article.id}/')
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Article.objects.filter(pk=self.article.pk).exists())

    def test_editor_can_approve_article(self):
        """Editor approval marks article approved and calls callback."""
        article = Article.objects.create(
            title='Needs approval',
            content='Body',
            author=self.journalist)
        client = self.client_class()
        client.force_login(self.editor)
        with patch('news_app.views.requests.post') as mocked_post:
            response = client.get(f'/approve-article/{article.id}/')
        self.assertEqual(response.status_code, 302)
        approved_article = Article.objects.get(pk=article.pk)
        self.assertTrue(approved_article.approved)
        mocked_post.assert_called_once()
