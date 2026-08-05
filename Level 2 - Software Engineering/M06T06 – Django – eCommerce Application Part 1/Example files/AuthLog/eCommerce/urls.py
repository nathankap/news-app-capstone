from django.urls import path
from . import views

app_name = 'eCommerce'

urlpatterns = [
    path('', views.list_products, name='products_list'),
    path('product/search/', views.view_product_page, name='product_page'),
    path('product/add/', views.add_product, name='add_product'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('product/<int:product_id>/edit/', views.edit_product, name='edit_product'),
    path('product/<int:product_id>/delete/', views.delete_product, name='delete_product'),
    path('product/<int:product_id>/review/', views.review_product, name='review_product'),
    path('add-to-cart/', views.add_item_to_cart, name='add_to_cart'),
    path('cart/', views.show_user_cart, name='main_cart_page'),
    path('checkout/', views.checkout, name='checkout'),
    path('clear-cart/', views.clear_cart, name='clear_cart'),
    path('change-price/', views.change_product_price, name='change_price'),
]
