# posts/tests.py
from django.test import TestCase
from django.urls import reverse
from .models import Note


class NoteModelTest(TestCase):
    def test_note_creation(self):
        note = Note.objects.create(
            title='Test Note',
            content='This is a test note.',
        )
        self.assertEqual(note.title, 'Test Note')
        self.assertEqual(note.content, 'This is a test note.')
        self.assertIsNotNone(note.created_at)

    def test_note_str(self):
        note = Note.objects.create(
            title='String Test',
            content='Content does not matter.',
        )
        self.assertEqual(str(note), 'String Test')


class NoteViewTest(TestCase):
    def setUp(self):
        self.note = Note.objects.create(
            title='Test Note',
            content='This is a test note.',
        )

    def test_note_list_view(self):
        response = self.client.get(reverse('note_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Note')
        self.assertContains(response, 'Add note')

    def test_note_detail_view(self):
        response = self.client.get(reverse('note_detail', args=[self.note.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Note')
        self.assertContains(response, 'This is a test note.')

    def test_note_create_view(self):
        response = self.client.post(
            reverse('note_create'),
            data={'title': 'Created Note', 'content': 'Created via form.'},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Created Note')
        self.assertEqual(Note.objects.filter(title='Created Note').count(), 1)

    def test_note_update_view(self):
        response = self.client.post(
            reverse('note_update', args=[self.note.pk]),
            data={'title': 'Updated Note', 'content': 'Updated content.'},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Updated Note')
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, 'Updated Note')
        self.assertEqual(self.note.content, 'Updated content.')

    def test_note_delete_view(self):
        response = self.client.get(reverse('note_delete', args=[self.note.pk]), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Note.objects.filter(pk=self.note.pk).exists())
