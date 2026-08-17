from django.urls import path
from . import views

app_name = 'eCommerce'

urlpatterns = [
    path('', views.list_products, name='products_list'),
    path('vendors/', views.list_vendors, name='vendors_list'),
    path('vendors/<int:vendor_id>/stores/', views.vendor_stores, name='vendor_stores'),
    path('reddit/', views.reddit_feed, name='reddit_feed'),
    path('product/search/', views.view_product_page, name='product_page'),
    path('product/add/', views.add_product, name='add_product'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('product/<int:product_id>/edit/', views.edit_product, name='edit_product'),
    path('product/<int:product_id>/delete/', views.delete_product, name='delete_product'),
    path('product/<int:product_id>/review/', views.review_product, name='review_product'),
    path('stores/<int:store_id>/products/', views.store_products, name='store_products'),
    path('add-to-cart/', views.add_item_to_cart, name='add_to_cart'),
    path('cart/', views.show_user_cart, name='main_cart_page'),
    path('checkout/', views.checkout, name='checkout'),
    path('clear-cart/', views.clear_cart, name='clear_cart'),
    path('change-price/', views.change_product_price, name='change_price'),
    path('stores/', views.list_stores, name='stores_list'),
    path('reviews/', views.vendor_reviews, name='vendor_reviews'),
    path('api/vendors/', views.api_vendors, name='api_vendors'),
    path('api/vendors/reviews/', views.api_vendor_reviews, name='api_vendor_reviews'),
    path('api/vendors/<int:vendor_id>/stores/', views.api_vendor_stores, name='api_vendor_stores'),
    path('api/stores/', views.api_stores, name='api_stores'),
    path('api/stores/<int:store_id>/products/', views.api_store_products, name='api_store_products'),
    path('api/products/', views.api_products, name='api_products'),
    path('api/products/<int:product_id>/reviews/', views.api_product_reviews, name='api_product_reviews'),
    path('stores/create/', views.create_store, name='create_store'),
    path('stores/<int:store_id>/edit/', views.edit_store, name='edit_store'),
    path('stores/<int:store_id>/delete/', views.delete_store, name='delete_store'),
]
