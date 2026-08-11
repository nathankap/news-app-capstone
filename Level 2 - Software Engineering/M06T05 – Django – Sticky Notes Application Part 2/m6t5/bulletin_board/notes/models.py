from django.db import models


class Note(models.Model):
    """Model representing a sticky note.

    Fields:
    - title: CharField for the note title.
    - content: TextField for the note content.
    - created_at: DateTimeField automatically set when the note is created.
    """
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
