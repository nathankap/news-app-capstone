# posts/forms.py
from django import forms

from .models import Note


class NoteForm(forms.ModelForm):
    """
    Form for creating and updating Note objects.
    Fields:
    - title: CharField for the note title.
    - content: TextField for the note content.
    """

    class Meta:
        model = Note
        fields = ["title", "content"]
