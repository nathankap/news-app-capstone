import requests
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.urls import reverse
from django.views.decorators.http import require_POST
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .forms import (
    ArticleForm,
    CustomAuthenticationForm,
    NewsletterForm,
    RegisterForm,
    PublisherForm,
    SubscriptionForm,
)
from .models import Article, CustomUser, Newsletter
from .serializers import ArticleSerializer, NewsletterSerializer


def home(request):
    """Render the homepage with approved articles and recent newsletters."""
    articles = Article.objects.filter(
        approved=True
    ).order_by('-created_at')[:8]
    newsletters = Newsletter.objects.order_by('-created_at')[:8]
    is_editor = _user_is_editor(request.user)
    return render(request, 'news_app/home.html', {
        'title': 'News App',
        'articles': articles,
        'newsletters': newsletters,
        'is_editor': is_editor,
        'is_journalist': _user_is_journalist(request.user),
    })


def register_view(request):
    """Register a new user account from the website."""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Account created successfully.')
            login(request, user)
            return redirect('dashboard')
    else:
        form = RegisterForm()

    return render(request, 'news_app/auth_form.html', {
        'title': 'Create Account',
        'form': form,
        'submit_label': 'Register',
    })


def login_view(request):
    """Authenticate a user from the website login page."""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('dashboard')
    else:
        form = CustomAuthenticationForm(request)

    return render(request, 'news_app/auth_form.html', {
        'title': 'Login',
        'form': form,
        'submit_label': 'Login',
    })


@login_required
def logout_view(request):
    """Log out current user and return to home."""
    logout(request)
    return redirect('home')


@login_required
def dashboard_view(request):
    """Render role-aware dashboard actions and user content."""
    user = request.user
    context = {
        'pending_articles': Article.objects.filter(approved=False).order_by(
            '-created_at'
        )[:10] if _user_is_editor(user) else [],
        'my_articles': Article.objects.filter(author=user).order_by(
            '-created_at'
        )[:10],
        'my_newsletters': Newsletter.objects.filter(author=user).order_by(
            '-created_at'
        )[:10],
        'is_editor': _user_is_editor(user),
        'is_journalist': _user_is_journalist(user),
        'is_reader': _user_has_role(user, 'reader'),
    }
    return render(request, 'news_app/dashboard.html', context)


def article_page(request, article_id):
    """Render a standalone page for a single article."""
    article = get_object_or_404(Article, id=article_id)
    if not article.approved and not (
        _user_is_editor(request.user)
        or (
            request.user.is_authenticated
            and article.author_id == request.user.id
        )
    ):
        return HttpResponseForbidden('This article is not publicly available.')

    return render(request, 'news_app/article_page.html', {'article': article})


def newsletter_page(request, newsletter_id):
    """Render a standalone page for a single newsletter."""
    newsletter = get_object_or_404(Newsletter, id=newsletter_id)
    return render(
        request,
        'news_app/newsletter_page.html',
        {'newsletter': newsletter},
    )


@login_required
def publisher_create_view(request):
    """Allow editors to create publishers and assign team members."""
    if not _user_is_editor(request.user):
        return HttpResponseForbidden('Only editors can manage publishers.')

    if request.method == 'POST':
        form = PublisherForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Publisher created successfully.')
            return redirect('dashboard')
    else:
        form = PublisherForm()

    return render(request, 'news_app/content_form.html', {
        'title': 'Create Publisher',
        'form': form,
        'submit_label': 'Create Publisher',
    })


@login_required
def article_create_view(request):
    """Allow journalists to create new articles via website form."""
    if not _user_is_journalist(request.user):
        return HttpResponseForbidden('Only journalists can create articles.')

    if request.method == 'POST':
        form = ArticleForm(request.POST, user=request.user)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.approved = False
            article.publisher = form.cleaned_data['publisher']
            article.save()
            messages.success(
                request,
                'Article created and submitted for editor approval.',
            )
            return redirect('dashboard')
    else:
        form = ArticleForm(user=request.user)

    return render(request, 'news_app/content_form.html', {
        'title': 'Create Article',
        'form': form,
        'submit_label': 'Create Article',
    })


@login_required
def article_edit_view(request, article_id):
    """Allow editors and owner journalists to edit article content."""
    article = get_object_or_404(Article, id=article_id)
    is_editor = _user_is_editor(request.user)
    is_owner_journalist = (
        _user_is_journalist(request.user)
        and article.author_id == request.user.id
    )

    if not (is_editor or is_owner_journalist):
        return HttpResponseForbidden('You cannot edit this article.')

    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article, user=request.user)
        if form.is_valid():
            updated_article = form.save(commit=False)
            if is_owner_journalist:
                updated_article.approved = False
            updated_article.save()
            updated_article.publisher = form.cleaned_data['publisher']
            updated_article.save(update_fields=['publisher'])
            messages.success(request, 'Article updated successfully.')
            return redirect('dashboard')
    else:
        form = ArticleForm(instance=article, user=request.user)

    return render(request, 'news_app/content_form.html', {
        'title': 'Edit Article',
        'form': form,
        'submit_label': 'Save Article',
    })


@login_required
def newsletter_create_view(request):
    """Allow journalists and editors to create newsletters."""
    if not (
        _user_is_journalist(request.user)
        or _user_is_editor(request.user)
    ):
        return HttpResponseForbidden(
            'Only journalists and editors can create newsletters.'
        )

    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            newsletter = form.save(commit=False)
            newsletter.author = request.user
            newsletter.save()
            form.save_m2m()
            messages.success(request, 'Newsletter created successfully.')
            return redirect('dashboard')
    else:
        form = NewsletterForm()

    return render(request, 'news_app/content_form.html', {
        'title': 'Create Newsletter',
        'form': form,
        'submit_label': 'Create Newsletter',
    })


@login_required
def newsletter_edit_view(request, newsletter_id):
    """Allow editors and owner journalists to edit newsletters."""
    newsletter = get_object_or_404(Newsletter, id=newsletter_id)
    is_editor = _user_is_editor(request.user)
    is_owner_journalist = (
        _user_is_journalist(request.user)
        and newsletter.author_id == request.user.id
    )

    if not (is_editor or is_owner_journalist):
        return HttpResponseForbidden('You cannot edit this newsletter.')

    if request.method == 'POST':
        form = NewsletterForm(request.POST, instance=newsletter)
        if form.is_valid():
            form.save()
            messages.success(request, 'Newsletter updated successfully.')
            return redirect('dashboard')
    else:
        form = NewsletterForm(instance=newsletter)

    return render(request, 'news_app/content_form.html', {
        'title': 'Edit Newsletter',
        'form': form,
        'submit_label': 'Save Newsletter',
    })


@login_required
@require_POST
def article_delete_view(request, article_id):
    """Delete an article for an editor or its journalist author."""
    article = get_object_or_404(Article, id=article_id)
    if not (
        _user_is_editor(request.user)
        or (
            _user_is_journalist(request.user)
            and article.author_id == request.user.id
        )
    ):
        return HttpResponseForbidden('You cannot delete this article.')
    article.delete()
    messages.success(request, 'Article deleted successfully.')
    return redirect('dashboard')


@login_required
@require_POST
def newsletter_delete_view(request, newsletter_id):
    """Delete a newsletter for an editor or its journalist author."""
    newsletter = get_object_or_404(Newsletter, id=newsletter_id)
    if not (
        _user_is_editor(request.user)
        or (
            _user_is_journalist(request.user)
            and newsletter.author_id == request.user.id
        )
    ):
        return HttpResponseForbidden('You cannot delete this newsletter.')
    newsletter.delete()
    messages.success(request, 'Newsletter deleted successfully.')
    return redirect('dashboard')


@login_required
def subscription_view(request):
    """Allow readers to manage publisher and journalist subscriptions."""
    if not _user_has_role(request.user, 'reader'):
        return HttpResponseForbidden('Only readers can manage subscriptions.')

    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            request.user.subscribed_publishers.set(
                form.cleaned_data['publishers']
            )
            request.user.subscribed_journalists.set(
                form.cleaned_data['journalists']
            )
            messages.success(request, 'Subscriptions updated.')
            next_url = request.POST.get('next')
            if next_url and url_has_allowed_host_and_scheme(
                next_url,
                allowed_hosts={request.get_host()},
                require_https=request.is_secure(),
            ):
                return redirect(next_url)
            return redirect('dashboard')
    else:
        form = SubscriptionForm(initial={
            'publishers': request.user.subscribed_publishers.all(),
            'journalists': request.user.subscribed_journalists.all(),
        })

    return render(request, 'news_app/content_form.html', {
        'title': 'Manage Subscriptions',
        'form': form,
        'submit_label': 'Save Subscriptions',
    })


def _user_has_role(user, role_name):
    """Return True when the user role/group/superuser matches the role name."""
    if not user.is_authenticated:
        return False

    return (
        user.is_superuser
        or getattr(user, 'role', '') == role_name
        or user.groups.filter(name=role_name.title()).exists()
    )


def _user_is_editor(user):
    """Return whether the user has editor access."""
    return _user_has_role(user, 'editor')


def _user_is_journalist(user):
    """Return whether the user has journalist access."""
    return _user_has_role(user, 'journalist')


def _notify_approval(request, article):
    """POST approval metadata to the local REST endpoint."""
    target_url = request.build_absolute_uri(reverse('approved_log'))
    try:
        requests.post(target_url, json={
            'article_id': article.id,
            'title': article.title,
        }, timeout=2)
    except requests.RequestException:
        return False
    return True


def _email_approved_article(article):
    """Email approved article content to interested subscribers."""
    recipients = set(
        CustomUser.objects.filter(
            subscribed_journalists=article.author
        ).exclude(email='').values_list('email', flat=True)
    )

    if article.publisher_id:
        recipients.update(
            article.publisher.subscribers.exclude(email='').values_list(
                'email', flat=True
            )
        )

    if not recipients:
        return

    send_mail(
        subject=f'Approved Article: {article.title}',
        message=(
            f'Title: {article.title}\n\n'
            f'Author: {article.author.username}\n\n'
            f'{article.content}'
        ),
        from_email=None,
        recipient_list=sorted(recipients),
        fail_silently=True,
    )


def editor_review_queue(request):
    """Render the editor queue for pending article approvals."""
    if not _user_is_editor(request.user):
        return HttpResponseForbidden('Only editors can review articles.')

    articles = Article.objects.order_by('-created_at')
    return render(
        request,
        'news_app/editor_review.html',
        {'articles': articles},
    )


@require_POST
def approve_article(request, article_id):
    """Approve an article and trigger subscriber notifications."""
    article = get_object_or_404(Article, id=article_id)

    if not _user_is_editor(request.user):
        return HttpResponseForbidden('Only editors can approve articles.')

    if not article.approved:
        article.approved = True
        article.save(update_fields=['approved'])
        _email_approved_article(article)
        _notify_approval(request, article)
        messages.success(request, 'Article approved successfully.')

    return redirect('editor_review_queue')


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def article_list_create(request):
    """List approved articles or create a new article as a journalist."""
    if request.method == 'GET':
        articles = Article.objects.filter(
            approved=True).order_by('-created_at')
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

    if not _user_is_journalist(request.user):
        return Response({'detail': 'Only journalists can create articles.'},
                        status=status.HTTP_403_FORBIDDEN)

    serializer = ArticleSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(author=request.user, approved=False)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def article_subscribed(request):
    """Return approved articles that match the reader subscriptions."""
    if not _user_has_role(request.user, 'reader'):
        return Response(
            {'detail': 'Only readers can use subscribed articles view.'},
            status=status.HTTP_403_FORBIDDEN,
        )

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
        if (
            not article.approved
            and not _user_is_editor(request.user)
            and article.author_id != request.user.id
        ):
            return Response(
                {'detail': 'Article is not approved.'},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    is_editor = _user_is_editor(request.user)
    is_journalist = _user_is_journalist(request.user)

    if not (is_editor or is_journalist):
        return Response(
            {
                'detail': 'Only journalists and editors can modify articles.'},
            status=status.HTTP_403_FORBIDDEN)

    if is_journalist and article.author_id != request.user.id:
        return Response(
            {'detail': 'Journalists can only modify their own articles.'},
            status=status.HTTP_403_FORBIDDEN,
        )

    if request.method == 'PUT':
        if is_journalist and 'approved' in request.data:
            return Response(
                {'detail': 'Only editors can approve articles.'},
                status=status.HTTP_403_FORBIDDEN,
            )
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
    """Receive approved article callbacks from internal integrations."""
    return Response({'detail': 'approved article logged',
                     'article_id': request.data.get('article_id')},
                    status=status.HTTP_201_CREATED)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def newsletter_list_create(request):
    """List newsletters or create one as journalist/editor."""
    if request.method == 'GET':
        newsletters = Newsletter.objects.all()
        serializer = NewsletterSerializer(newsletters, many=True)
        return Response(serializer.data)

    if not (
        _user_is_journalist(request.user)
        or _user_is_editor(request.user)
    ):
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


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def newsletter_detail(request, newsletter_id):
    """Retrieve, update, or delete a newsletter based on role rules."""
    newsletter = get_object_or_404(Newsletter, id=newsletter_id)

    if request.method == 'GET':
        serializer = NewsletterSerializer(newsletter)
        return Response(serializer.data)

    is_editor = _user_is_editor(request.user)
    is_journalist = _user_is_journalist(request.user)
    if not (is_editor or is_journalist):
        return Response(
            {'detail': 'Only journalists and editors can modify newsletters.'},
            status=status.HTTP_403_FORBIDDEN,
        )

    if is_journalist and newsletter.author_id != request.user.id:
        return Response(
            {'detail': 'Journalists can only modify their own newsletters.'},
            status=status.HTTP_403_FORBIDDEN,
        )

    if request.method == 'PUT':
        serializer = NewsletterSerializer(
            newsletter,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    newsletter.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
