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
            'Editors can manage publishers and approve submitted articles.'
        )

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if CustomUser.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                'An account with this email already exists.'
            )
        return email


class PublisherForm(forms.ModelForm):
    """Form for editors to create publishers and assign their members."""

    class Meta:
        model = Publisher
        fields = ['name', 'editors', 'journalists']
        widgets = {
            'editors': forms.CheckboxSelectMultiple,
            'journalists': forms.CheckboxSelectMultiple,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['editors'].queryset = CustomUser.objects.filter(
            role='editor'
        )
        self.fields['journalists'].queryset = CustomUser.objects.filter(
            role='journalist'
        )


class ArticleForm(forms.ModelForm):
    """Website form for journalist article creation and editing."""

    publisher = forms.ModelChoiceField(
        queryset=Publisher.objects.none(),
        required=False,
        empty_label='Independent',
        label='Publisher (optional)',
    )

    class Meta:
        model = Article
        fields = ['title', 'content']

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user is not None and user.role == 'journalist':
            self.fields['publisher'].queryset = Publisher.objects.filter(
                journalists=user
            ).order_by('name')
        elif user is not None:
            self.fields['publisher'].queryset = Publisher.objects.order_by(
                'name'
            )
        elif self.instance and self.instance.publisher_id:
            self.fields['publisher'].queryset = Publisher.objects.filter(
                pk=self.instance.publisher_id
            )
        if self.instance and self.instance.pk:
            self.fields['publisher'].initial = self.instance.publisher_id


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
