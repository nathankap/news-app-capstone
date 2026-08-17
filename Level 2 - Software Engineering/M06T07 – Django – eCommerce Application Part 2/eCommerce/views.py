import json
from decimal import Decimal, InvalidOperation

from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.conf import settings
from .models import Product, Order, OrderItem, Review, Store
from functions.reddit import fetch_reddit_posts


def is_vendor(user):
    return user.is_authenticated and (
        user.is_superuser or user.groups.filter(
            name='Vendors').exists())


def is_buyer(user):
    return user.is_authenticated and user.groups.filter(name='Buyers').exists()


def user_stores(user):
    if not user.is_authenticated:
        return Store.objects.none()
    return Store.objects.filter(owner=user)


def cart_items_from_session(request):
    cart = request.session.get('cart', {})
    items = []
    for product_id, quantity in cart.items():
        try:
            product = Product.objects.get(pk=int(product_id))
            items.append({'product': product, 'quantity': quantity,
                         'subtotal': product.price * quantity})
        except (Product.DoesNotExist, ValueError):
            continue
    return items


def list_products(request):
    products = Product.objects.all()
    return render(request, 'eCommerce/products_list.html', {
        'products': products,
        'page_title': 'All Products',
        'is_vendor': is_vendor(request.user),
        'is_buyer': is_buyer(request.user),
    })


def list_vendors(request):
    """Show vendors so buyers can browse each vendor's stores."""
    user_model = get_user_model()
    vendors = user_model.objects.filter(
        groups__name='Vendors'
    ).distinct().order_by('username')
    return render(request, 'eCommerce/vendors_list.html', {
        'vendors': vendors,
    })


def reddit_feed(request):
    try:
        posts = fetch_reddit_posts('django', limit=10)
    except Exception:
        posts = []
    return render(request, 'eCommerce/reddit_feed.html', {'posts': posts})


def view_product_page(request):
    if request.method == 'POST':
        product_name = request.POST.get('product')
        if not product_name:
            return render(request, 'eCommerce/product_page.html',
                          {'error': 'Please enter a product name.'})
        try:
            product = Product.objects.get(name__icontains=product_name)
            return render(request,
                          'eCommerce/product_page.html',
                          {'product': product})
        except Product.DoesNotExist:
            return render(request,
                          'eCommerce/product_page.html',
                          {'error': 'Product not found.'})
    return render(request, 'eCommerce/product_page.html')


def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    reviews = product.reviews.all()
    return render(request, 'eCommerce/product_detail.html', {
        'product': product,
        'reviews': reviews,
        'is_vendor': is_vendor(request.user),
        'is_buyer': is_buyer(request.user),
    })


def vendor_stores(request, vendor_id):
    """Show all stores owned by a selected vendor."""
    vendor = get_object_or_404(
        get_user_model(),
        pk=vendor_id,
        groups__name='Vendors',
    )
    stores = Store.objects.filter(owner=vendor).order_by('name')
    return render(request, 'eCommerce/stores_list.html', {
        'stores': stores,
        'vendor': vendor,
        'is_vendor': is_vendor(request.user),
        'manage_stores': False,
    })


def store_products(request, store_id):
    """Show products belonging to one store."""
    store = get_object_or_404(Store, pk=store_id)
    products = Product.objects.filter(store=store)
    return render(request, 'eCommerce/products_list.html', {
        'products': products,
        'page_title': f'Products in {store.name}',
        'store': store,
        'is_vendor': is_vendor(request.user),
        'is_buyer': is_buyer(request.user),
    })


@login_required(login_url='/')
def add_product(request):
    if not is_vendor(request.user):
        return render(request, 'eCommerce/add_product.html',
                      {'error': 'Only vendors can add products.'})

    stores = user_stores(request.user)
    if not stores.exists():
        return render(request, 'eCommerce/add_product.html',
                      {'error': 'Create a store before adding products.'})

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        store_id = request.POST.get('store_id')

        if not name or not price or not stock or not store_id:
            return render(request,
                          'eCommerce/add_product.html',
                          {'error': 'Name, price, stock, and a store are required.',
                           'stores': stores})

        try:
            price = float(price)
            stock = int(stock)
            store = stores.get(pk=store_id)
        except (ValueError, Store.DoesNotExist):
            return render(request,
                          'eCommerce/add_product.html',
                          {'error': 'Price, stock, and store selection must be valid.',
                           'stores': stores})

        Product.objects.create(
            vendor=request.user,
            store=store,
            name=name,
            description=description,
            price=price,
            stock=stock)
        return HttpResponseRedirect(reverse('eCommerce:products_list'))

    return render(request, 'eCommerce/add_product.html', {'stores': stores})


@login_required(login_url='/')
def edit_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if product.vendor != request.user and (
            product.store is None or product.store.owner != request.user):
        return render(request,
                      'eCommerce/edit_product.html',
                      {'error': 'You can only edit your own products.',
                       'product': product})

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        price = request.POST.get('price')
        stock = request.POST.get('stock')

        if not name or not price or not stock:
            return render(request,
                          'eCommerce/edit_product.html',
                          {'error': 'All fields are required.',
                           'product': product})

        try:
            product.price = float(price)
            product.stock = int(stock)
        except ValueError:
            return render(request,
                          'eCommerce/edit_product.html',
                          {'error': 'Price and stock must be valid numbers.',
                           'product': product})

        product.name = name
        product.description = description
        product.save()
        return HttpResponseRedirect(
            reverse(
                'eCommerce:product_detail',
                kwargs={
                    'product_id': product.id}))

    return render(request, 'eCommerce/edit_product.html', {'product': product})


@login_required(login_url='/')
def change_product_price(request):
    if not is_vendor(request.user):
        return render(request, 'eCommerce/change_price.html',
                      {'error': 'Only vendors can change product prices.'})

    if request.method == 'POST':
        product_name = request.POST.get('product')
        new_price = request.POST.get('new_price')

        if not product_name or not new_price:
            return render(request, 'eCommerce/change_price.html', {
                'error': 'Please provide both product name and new price.'
            })

        try:
            product = Product.objects.get(
                name__iexact=product_name, vendor=request.user)
        except Product.DoesNotExist:
            return render(request, 'eCommerce/change_price.html', {
                'error': 'Product not found or not owned by you.'
            })

        try:
            product.price = float(new_price)
            product.save()
            return HttpResponseRedirect(
                reverse(
                    'eCommerce:product_detail',
                    kwargs={
                        'product_id': product.id}))
        except ValueError:
            return render(request, 'eCommerce/change_price.html', {
                'error': 'Invalid price format.'
            })

    return render(request, 'eCommerce/change_price.html')


@login_required(login_url='/')
def delete_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if product.vendor != request.user and (
            product.store is None or product.store.owner != request.user):
        return render(request, 'eCommerce/confirm_delete.html', {
            'error': 'You can only delete your own products.',
            'product': product,
        })

    if request.method == 'POST':
        product.delete()
        return HttpResponseRedirect(reverse('eCommerce:products_list'))

    return render(request,
                  'eCommerce/confirm_delete.html',
                  {'product': product})


@login_required(login_url='/')
def review_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment', '')
        try:
            rating = int(rating)
            if rating < 1 or rating > 5:
                raise ValueError
        except (ValueError, TypeError):
            return render(request,
                          'eCommerce/review_product.html',
                          {'product': product,
                           'error': 'Rating must be a number between 1 and 5.'})

        Review.objects.create(
            product=product,
            user=request.user,
            rating=rating,
            comment=comment)
        return HttpResponseRedirect(
            reverse(
                'eCommerce:product_detail',
                kwargs={
                    'product_id': product.id}))

    return render(request,
                  'eCommerce/review_product.html',
                  {'product': product})


def add_item_to_cart(request):
    if request.method != 'POST':
        return redirect('eCommerce:products_list')

    product_id = request.POST.get('product_id')
    quantity = request.POST.get('quantity', '1')

    try:
        product = Product.objects.get(pk=int(product_id))
    except (Product.DoesNotExist, ValueError, TypeError):
        return redirect('eCommerce:products_list')

    try:
        quantity = int(quantity)
        if quantity < 1:
            quantity = 1
    except ValueError:
        quantity = 1

    cart = request.session.get('cart', {})
    cart[str(product.id)] = cart.get(str(product.id), 0) + quantity
    request.session['cart'] = cart
    request.session.modified = True

    return redirect(reverse('eCommerce:main_cart_page'))


def show_user_cart(request):
    cart_items = cart_items_from_session(request)
    total_price = sum(item['subtotal'] for item in cart_items)
    return render(request, 'eCommerce/main_cart_page.html', {
        'cart': cart_items,
        'total_price': total_price,
    })


@login_required(login_url='/')
def checkout(request):
    cart_items = cart_items_from_session(request)
    if not cart_items:
        return render(request,
                      'eCommerce/main_cart_page.html',
                      {'cart': [],
                       'total_price': 0,
                       'error': 'Your cart is empty.'})

    if request.method == 'POST':
        order = Order.objects.create(user=request.user)
        total_price = 0

        for item in cart_items:
            product = item['product']
            quantity = item['quantity']
            if quantity > product.stock:
                return render(request, 'eCommerce/main_cart_page.html', {
                    'cart': cart_items,
                    'total_price': sum(i['subtotal'] for i in cart_items),
                    'error': f'Not enough stock for {product.name}.',
                })
            price = product.price
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=price)
            total_price += price * quantity
            product.stock -= quantity
            product.save()

        order.total_price = total_price
        order.save()
        send_order_email(order)
        request.session['cart'] = {}
        request.session.modified = True

        return render(request,
                      'eCommerce/checkout_success.html',
                      {'order': order})

    return render(request,
                  'eCommerce/checkout.html',
                  {'cart': cart_items,
                   'total_price': sum(item['subtotal'] for item in cart_items)})


def send_order_email(order):
    lines = [
        f'Invoice for Order #{
            order.pk}', f'Customer: {
            order.user.username}', '']
    for item in order.items.all():
        lines.append(
            f'- {item.product.name} x {item.quantity} @ R{item.price} = R{item.price * item.quantity}')
    lines.append('')
    lines.append(f'Total: R{order.total_price}')
    lines.append('Thank you for your purchase!')

    email = EmailMessage(
        subject=f'Order Confirmation #{order.pk}',
        body='\n'.join(lines),
        from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'no-reply@authlog.local'),
        to=[order.user.email],
    )
    email.send()
    order.email_sent = True
    order.save()


def clear_cart(request):
    request.session['cart'] = {}
    request.session.modified = True
    return redirect('eCommerce:main_cart_page')


def list_stores(request):
    """Show every store, with management links for its owner."""
    stores = Store.objects.select_related('owner').order_by('name')
    return render(request, 'eCommerce/stores_list.html', {
        'stores': stores,
        'is_vendor': is_vendor(request.user),
        'manage_stores': True,
    })


@login_required(login_url='/')
def vendor_reviews(request):
    """Show a vendor's reviews as one list grouped by product context."""
    if not is_vendor(request.user):
        return redirect('grabsomore:welcome')
    reviews = Review.objects.filter(
        product__store__owner=request.user
    ).select_related('product', 'product__store', 'user')
    return render(request, 'eCommerce/vendor_reviews.html', {
        'reviews': reviews,
    })


@login_required(login_url='/')
def create_store(request):
    if not is_vendor(request.user):
        return redirect('grabsomore:welcome')

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        description = request.POST.get('description', '').strip()
        if not name:
            return render(request, 'eCommerce/store_form.html',
                          {'error': 'Store name is required.'})
        Store.objects.create(
            owner=request.user,
            name=name,
            description=description)
        return redirect('eCommerce:stores_list')

    return render(request, 'eCommerce/store_form.html')


@login_required(login_url='/')
def edit_store(request, store_id):
    if not is_vendor(request.user):
        return redirect('grabsomore:welcome')
    store = get_object_or_404(Store, pk=store_id, owner=request.user)

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        description = request.POST.get('description', '').strip()
        if not name:
            return render(request, 'eCommerce/store_form.html',
                          {'store': store, 'error': 'Store name is required.'})
        store.name = name
        store.description = description
        store.save()
        return redirect('eCommerce:stores_list')

    return render(request, 'eCommerce/store_form.html', {'store': store})


@login_required(login_url='/')
def delete_store(request, store_id):
    if not is_vendor(request.user):
        return redirect('grabsomore:welcome')
    store = get_object_or_404(Store, pk=store_id, owner=request.user)

    if request.method == 'POST':
        store.delete()
        return redirect('eCommerce:stores_list')

    return render(request,
                  'eCommerce/store_confirm_delete.html',
                  {'store': store})


def api_store_data(store):
    """Return the public JSON representation of a store."""
    return {
        'id': store.id,
        'name': store.name,
        'description': store.description,
        'owner_id': store.owner_id,
        'owner': store.owner.username,
        'created_at': store.created_at.isoformat(),
    }


def api_product_data(product):
    """Return the public JSON representation of a product."""
    return {
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'price': str(product.price),
        'stock': product.stock,
        'vendor_id': product.vendor_id,
        'store_id': product.store_id,
    }


def api_review_data(review):
    """Return the public JSON representation of a review."""
    return {
        'id': review.id,
        'product_id': review.product_id,
        'product': review.product.name,
        'user': review.user.username,
        'rating': review.rating,
        'comment': review.comment,
        'verified': review.verified,
        'created_at': review.created_at.isoformat(),
    }


def api_vendors(request):
    """List vendors for the vendor-to-stores retrieval path."""
    vendors = get_user_model().objects.filter(
        groups__name='Vendors'
    ).distinct().order_by('username')
    return JsonResponse({
        'vendors': [
            {'id': vendor.id, 'username': vendor.username}
            for vendor in vendors
        ]
    })


def api_vendor_stores(request, vendor_id):
    """List stores for a selected vendor."""
    vendor = get_object_or_404(
        get_user_model(), pk=vendor_id, groups__name='Vendors')
    stores = Store.objects.filter(owner=vendor).select_related('owner')
    return JsonResponse({
        'vendor': vendor.username,
        'stores': [api_store_data(store) for store in stores],
    })


def api_stores(request):
    """List all stores or create one for the authenticated vendor."""
    if request.method == 'GET':
        stores = Store.objects.select_related('owner').order_by('name')
        return JsonResponse({
            'stores': [api_store_data(store) for store in stores],
        })

    if not is_vendor(request.user):
        return JsonResponse({'error': 'Vendor login required.'}, status=403)

    try:
        payload = json.loads(request.body or '{}')
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Request body must be JSON.'}, status=400)

    name = str(payload.get('name', '')).strip()
    if not name:
        return JsonResponse({'error': 'Store name is required.'}, status=400)
    store = Store.objects.create(
        owner=request.user,
        name=name,
        description=str(payload.get('description', '')).strip(),
    )
    return JsonResponse(api_store_data(store), status=201)


def api_store_products(request, store_id):
    """List products for a store or add one for its vendor owner."""
    store = get_object_or_404(Store.objects.select_related('owner'), pk=store_id)
    if request.method == 'GET':
        products = Product.objects.filter(store=store).order_by('name')
        return JsonResponse({
            'store': api_store_data(store),
            'products': [api_product_data(product) for product in products],
        })

    if not is_vendor(request.user) or store.owner_id != request.user.id:
        return JsonResponse(
            {'error': 'Only the store owner can add products.'},
            status=403,
        )
    try:
        payload = json.loads(request.body or '{}')
        price = Decimal(str(payload.get('price', '')))
        stock = int(payload.get('stock', -1))
    except (json.JSONDecodeError, InvalidOperation, TypeError, ValueError):
        return JsonResponse(
            {'error': 'Price and stock must be valid values.'}, status=400)

    name = str(payload.get('name', '')).strip()
    if not name or price < 0 or stock < 0:
        return JsonResponse(
            {'error': 'Name, non-negative price, and stock are required.'},
            status=400,
        )
    product = Product.objects.create(
        vendor=request.user,
        store=store,
        name=name,
        description=str(payload.get('description', '')).strip(),
        price=price,
        stock=stock,
    )
    return JsonResponse(api_product_data(product), status=201)


def api_products(request):
    """List all products for the direct product retrieval path."""
    products = Product.objects.all().order_by('name')
    return JsonResponse({
        'products': [api_product_data(product) for product in products],
    })


def api_product_reviews(request, product_id):
    """List reviews for one product."""
    product = get_object_or_404(Product, pk=product_id)
    reviews = product.reviews.select_related('product', 'user').all()
    return JsonResponse({
        'product': api_product_data(product),
        'reviews': [api_review_data(review) for review in reviews],
    })


@login_required(login_url='/')
def api_vendor_reviews(request):
    """List every review for products owned by the authenticated vendor."""
    if not is_vendor(request.user):
        return JsonResponse({'error': 'Vendor login required.'}, status=403)
    reviews = Review.objects.filter(
        product__store__owner=request.user
    ).select_related('product', 'product__store', 'user')
    return JsonResponse({
        'reviews': [api_review_data(review) for review in reviews],
    })
