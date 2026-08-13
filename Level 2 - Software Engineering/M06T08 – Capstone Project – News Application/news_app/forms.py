from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import Article, CustomUser, Newsletter, Publisher


class CustomAuthenticationForm(AuthenticationForm):
    """Authentication form used for website login."""


class RegisterForm(UserCreationForm):
    """Registration form that allows choosing a user role."""

    email = forms.EmailField(required=True)

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'role', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['role'].help_text = (
            'Editor and journalist accounts require approval before use.'
        )


class ArticleForm(forms.ModelForm):
    """Website form for journalist article creation and editing."""

    publisher_members = forms.ModelMultipleChoiceField(
        queryset=CustomUser.objects.filter(role__in=['editor', 'journalist']),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label='Publisher Team (optional)',
        help_text=(
            'Select one or more editors/journalists to represent '
            'publisher content.'
        ),
    )

    class Meta:
        model = Article
        fields = ['title', 'content']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk and self.instance.publisher_id:
            publisher = self.instance.publisher
            initial_members = list(publisher.editors.all()) + list(
                publisher.journalists.all()
            )
            self.fields['publisher_members'].initial = initial_members


class NewsletterForm(forms.ModelForm):
    """Website form for newsletter creation and editing."""

    class Meta:
        model = Newsletter
        fields = ['title', 'description', 'articles']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['articles'].queryset = Article.objects.filter(
            approved=True
        )
        self.fields['articles'].required = False


class SubscriptionForm(forms.Form):
    """Reader subscription form for publishers and journalists."""

    publishers = forms.ModelMultipleChoiceField(
        queryset=Publisher.objects.all(),
        required=False,
    )
    journalists = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.filter(role='journalist'),
        required=False,
    )
