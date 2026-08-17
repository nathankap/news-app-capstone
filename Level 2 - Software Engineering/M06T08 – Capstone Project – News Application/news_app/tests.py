from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from .models import Article, Newsletter, Publisher


class NewsApiTests(TestCase):
    """API and workflow tests for the news application."""

    def setUp(self):
        """Create role users and seed publisher/article/newsletter data."""
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
        """Home page should render approved content lists."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Example')
        self.assertContains(response, 'Weekly')

    def test_editor_registration_is_immediately_available(self):
        """Editors can operate a blank database without account approval."""
        self.user_model.objects.all().delete()
        response = self.client.post('/register/', {
            'username': 'first-editor',
            'email': 'first@example.com',
            'role': 'editor',
            'password1': 'Password123!abc',
            'password2': 'Password123!abc',
        })
        self.assertEqual(response.status_code, 302)
        first_editor = self.user_model.objects.get(username='first-editor')
        self.assertEqual(first_editor.role, 'editor')

    def test_later_editor_registration_is_also_immediately_available(self):
        """Later elevated accounts do not require account approval."""
        response = self.client.post('/register/', {
            'username': 'second-editor',
            'email': 'second@example.com',
            'role': 'editor',
            'password1': 'Password123!abc',
            'password2': 'Password123!abc',
        })
        self.assertEqual(response.status_code, 302)
        second_editor = self.user_model.objects.get(username='second-editor')
        self.assertEqual(second_editor.role, 'editor')

    def test_editor_can_create_publisher_and_assign_members(self):
        """Editors can manage publisher membership in the website."""
        client = self.client_class()
        client.force_login(self.editor)
        response = client.post('/publishers/create/', {
            'name': 'News Desk',
            'editors': [self.editor.id],
            'journalists': [self.journalist.id],
        })
        self.assertEqual(response.status_code, 302)
        publisher = Publisher.objects.get(name='News Desk')
        self.assertIn(self.editor, publisher.editors.all())
        self.assertIn(self.journalist, publisher.journalists.all())

    def test_reader_can_list_approved_articles(self):
        """Readers can call the approved article listing endpoint."""
        self.client.force_authenticate(self.reader)
        response = self.client.get('/api/articles/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_unauthenticated_cannot_list_articles(self):
        """Unauthenticated requests should be rejected by token auth."""
        response = self.client.get('/api/articles/')
        self.assertEqual(response.status_code, 401)

    def test_journalist_can_create_article(self):
        """Journalists can create new unapproved articles."""
        self.client.force_authenticate(self.journalist)
        response = self.client.post('/api/articles/', {
            'title': 'New',
            'content': 'Content',
            'publisher': self.publisher.id,
        }, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertFalse(response.json()['approved'])

    def test_reader_cannot_create_article(self):
        """Readers cannot create articles."""
        self.client.force_authenticate(self.reader)
        response = self.client.post('/api/articles/', {
            'title': 'Blocked',
            'content': 'Nope',
        }, format='json')
        self.assertEqual(response.status_code, 403)

    def test_reader_can_list_only_subscribed_articles(self):
        """Subscribed endpoint returns only matching subscriptions."""
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

    def test_non_reader_cannot_access_subscribed_endpoint(self):
        """Only readers should use the subscribed endpoint."""
        self.client.force_authenticate(self.journalist)
        response = self.client.get('/api/articles/subscribed/')
        self.assertEqual(response.status_code, 403)

    def test_journalist_can_update_article(self):
        """Journalists can update their own articles."""
        self.client.force_authenticate(self.journalist)
        response = self.client.put(
            f'/api/articles/{self.article.id}/',
            {'title': 'Updated'},
            format='json')
        self.assertEqual(response.status_code, 200)
        self.article.refresh_from_db()
        self.assertEqual(self.article.title, 'Updated')

    def test_journalist_cannot_approve_via_put(self):
        """Journalists cannot set approved status through API updates."""
        self.client.force_authenticate(self.journalist)
        response = self.client.put(
            f'/api/articles/{self.article.id}/',
            {'approved': True},
            format='json',
        )
        self.assertEqual(response.status_code, 403)

    def test_editor_can_delete_article(self):
        """Editors can delete any article."""
        self.client.force_authenticate(self.editor)
        response = self.client.delete(f'/api/articles/{self.article.id}/')
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Article.objects.filter(pk=self.article.pk).exists())

    def test_reader_cannot_delete_article(self):
        """Readers cannot delete articles."""
        self.client.force_authenticate(self.reader)
        response = self.client.delete(f'/api/articles/{self.article.id}/')
        self.assertEqual(response.status_code, 403)

    def test_editor_can_approve_article(self):
        """Editor approval triggers callback and marks article approved."""
        article = Article.objects.create(
            title='Needs approval',
            content='Body',
            author=self.journalist)
        client = self.client_class()
        client.force_login(self.editor)
        with patch('news_app.views.requests.post') as mocked_post:
            response = client.post(f'/approve-article/{article.id}/')
        self.assertEqual(response.status_code, 302)
        approved_article = Article.objects.get(pk=article.pk)
        self.assertTrue(approved_article.approved)
        mocked_post.assert_called_once()

    def test_reader_cannot_approve_article(self):
        """Readers cannot use the approval workflow endpoint."""
        article = Article.objects.create(
            title='Awaiting review',
            content='Body',
            author=self.journalist,
        )
        client = self.client_class()
        client.force_login(self.reader)
        response = client.post(f'/approve-article/{article.id}/')
        self.assertEqual(response.status_code, 403)

    def test_newsletter_role_permissions(self):
        """Readers can view newsletters but cannot create them."""
        self.client.force_authenticate(self.reader)
        list_response = self.client.get('/api/newsletters/')
        self.assertEqual(list_response.status_code, 200)

        create_response = self.client.post('/api/newsletters/', {
            'title': 'Reader newsletter',
            'description': 'not allowed',
            'articles': [self.article.id],
        }, format='json')
        self.assertEqual(create_response.status_code, 403)

    def test_journalist_can_create_update_delete_own_newsletter(self):
        """Journalists can fully manage their own newsletters."""
        self.client.force_authenticate(self.journalist)
        create_response = self.client.post('/api/newsletters/', {
            'title': 'Tech Weekly',
            'description': 'Roundup',
            'articles': [self.article.id],
        }, format='json')
        self.assertEqual(create_response.status_code, 201)
        newsletter_id = create_response.json()['id']

        update_response = self.client.put(
            f'/api/newsletters/{newsletter_id}/',
            {'title': 'Tech Weekly Updated'},
            format='json',
        )
        self.assertEqual(update_response.status_code, 200)

        delete_response = self.client.delete(
            f'/api/newsletters/{newsletter_id}/'
        )
        self.assertEqual(delete_response.status_code, 204)
