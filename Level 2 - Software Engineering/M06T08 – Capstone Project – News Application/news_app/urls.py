from django.urls import path
from . import views

urlpatterns = [
    path(
        '',
        views.home,
        name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path(
        'publishers/create/',
        views.publisher_create_view,
        name='publisher_create',
    ),
    path(
        'articles/<int:article_id>/',
        views.article_page,
        name='article_page',
    ),
    path('articles/create/', views.article_create_view, name='article_create'),
    path(
        'articles/<int:article_id>/edit/',
        views.article_edit_view,
        name='article_edit',
    ),
    path(
        'articles/<int:article_id>/delete/',
        views.article_delete_view,
        name='article_delete',
    ),
    path(
        'newsletters/<int:newsletter_id>/',
        views.newsletter_page,
        name='newsletter_page',
    ),
    path(
        'newsletters/create/',
        views.newsletter_create_view,
        name='newsletter_create',
    ),
    path(
        'newsletters/<int:newsletter_id>/edit/',
        views.newsletter_edit_view,
        name='newsletter_edit',
    ),
    path(
        'newsletters/<int:newsletter_id>/delete/',
        views.newsletter_delete_view,
        name='newsletter_delete',
    ),
    path(
        'subscriptions/',
        views.subscription_view,
        name='subscriptions',
    ),
    path(
        'editor/review/',
        views.editor_review_queue,
        name='editor_review_queue'),
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
    path(
        'api/newsletters/<int:newsletter_id>/',
        views.newsletter_detail,
        name='newsletter_detail'),
]
