from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.conf import settings
from .models import Product, Order, OrderItem, Review, Store


def is_vendor(user):
    """Return True when the user has vendor privileges."""
    return user.is_authenticated and (user.is_superuser or user.groups.filter(name='Vendors').exists())


def is_buyer(user):
    """Return True when the user belongs to the buyers group."""
    return user.is_authenticated and user.groups.filter(name='Buyers').exists()


def user_stores(user):
    """Return stores owned by the authenticated user."""
    if not user.is_authenticated:
        return Store.objects.none()
    return Store.objects.filter(owner=user)


def cart_items_from_session(request):
    """Build a cart item list from session data."""
    cart = request.session.get('cart', {})
    items = []
    for product_id, quantity in cart.items():
        try:
            product = Product.objects.get(pk=int(product_id))
            items.append({'product': product, 'quantity': quantity, 'subtotal': product.price * quantity})
        except (Product.DoesNotExist, ValueError):
            continue
    return items


def list_products(request):
    """Render the product catalog page."""
    products = Product.objects.all()
    return render(request, 'eCommerce/products_list.html', {
        'products': products,
        'is_vendor': is_vendor(request.user),
        'is_buyer': is_buyer(request.user),
    })


def view_product_page(request):
    """Search for and display a single product by name."""
    context = {
        'is_vendor': is_vendor(request.user),
        'is_buyer': is_buyer(request.user),
    }
    if request.method == 'POST':
        product_name = request.POST.get('product')
        if not product_name:
            context['error'] = 'Please enter a product name.'
            return render(request, 'eCommerce/product_page.html', context)
        try:
            product = Product.objects.get(name__icontains=product_name)
            context['product'] = product
            return render(request, 'eCommerce/product_page.html', context)
        except Product.DoesNotExist:
            context['error'] = 'Product not found.'
            return render(request, 'eCommerce/product_page.html', context)
    return render(request, 'eCommerce/product_page.html', context)


def product_detail(request, product_id):
    """Render product details and reviews for a product."""
    product = get_object_or_404(Product, pk=product_id)
    reviews = product.reviews.all()
    return render(request, 'eCommerce/product_detail.html', {
        'product': product,
        'reviews': reviews,
        'is_vendor': is_vendor(request.user),
        'is_buyer': is_buyer(request.user),
    })


@login_required(login_url='/')
def add_product(request):
    """Allow a vendor to create a product in one of their stores."""
    if not is_vendor(request.user):
        return render(request, 'eCommerce/add_product.html', {'error': 'Only vendors can add products.'})

    stores = user_stores(request.user)
    if not stores.exists():
        return render(request, 'eCommerce/add_product.html', {'error': 'Create a store before adding products.'})

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        store_id = request.POST.get('store_id')

        if not name or not price or not stock or not store_id:
            return render(request, 'eCommerce/add_product.html', {'error': 'Name, price, stock, and a store are required.', 'stores': stores})

        try:
            price = float(price)
            stock = int(stock)
            store = stores.get(pk=store_id)
        except (ValueError, Store.DoesNotExist):
            return render(request, 'eCommerce/add_product.html', {'error': 'Price, stock, and store selection must be valid.', 'stores': stores})

        Product.objects.create(vendor=request.user, store=store, name=name, description=description, price=price, stock=stock)
        return HttpResponseRedirect(reverse('eCommerce:products_list'))

    return render(request, 'eCommerce/add_product.html', {'stores': stores})


@login_required(login_url='/')
def edit_product(request, product_id):
    """Allow a vendor to edit one of their own products."""
    product = get_object_or_404(Product, pk=product_id)
    if product.vendor != request.user and (product.store is None or product.store.owner != request.user):
        return render(request, 'eCommerce/edit_product.html', {'error': 'You can only edit your own products.', 'product': product})

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        price = request.POST.get('price')
        stock = request.POST.get('stock')

        if not name or not price or not stock:
            return render(request, 'eCommerce/edit_product.html', {'error': 'All fields are required.', 'product': product})

        try:
            product.price = float(price)
            product.stock = int(stock)
        except ValueError:
            return render(request, 'eCommerce/edit_product.html', {'error': 'Price and stock must be valid numbers.', 'product': product})

        product.name = name
        product.description = description
        product.save()
        return HttpResponseRedirect(reverse('eCommerce:product_detail', kwargs={'product_id': product.id}))

    return render(request, 'eCommerce/edit_product.html', {'product': product})


@login_required(login_url='/')
def change_product_price(request):
    """Allow a vendor to update a product price by product name."""
    if not is_vendor(request.user):
        return render(request, 'eCommerce/change_price.html', {'error': 'Only vendors can change product prices.'})

    if request.method == 'POST':
        product_name = request.POST.get('product')
        new_price = request.POST.get('new_price')

        if not product_name or not new_price:
            return render(request, 'eCommerce/change_price.html', {
                'error': 'Please provide both product name and new price.'
            })

        try:
            product = Product.objects.get(name__iexact=product_name, vendor=request.user)
        except Product.DoesNotExist:
            return render(request, 'eCommerce/change_price.html', {
                'error': 'Product not found or not owned by you.'
            })

        try:
            product.price = float(new_price)
            product.save()
            return HttpResponseRedirect(reverse('eCommerce:product_detail', kwargs={'product_id': product.id}))
        except ValueError:
            return render(request, 'eCommerce/change_price.html', {
                'error': 'Invalid price format.'
            })

    return render(request, 'eCommerce/change_price.html')


@login_required(login_url='/')
def delete_product(request, product_id):
    """Allow a vendor to delete one of their own products."""
    product = get_object_or_404(Product, pk=product_id)
    if product.vendor != request.user and (product.store is None or product.store.owner != request.user):
        return render(request, 'eCommerce/confirm_delete.html', {
            'error': 'You can only delete your own products.',
            'product': product,
        })

    if request.method == 'POST':
        product.delete()
        return HttpResponseRedirect(reverse('eCommerce:products_list'))

    return render(request, 'eCommerce/confirm_delete.html', {'product': product})


@login_required(login_url='/')
def review_product(request, product_id):
    """Allow a buyer to submit a review for a product."""
    if not is_buyer(request.user):
        return redirect('eCommerce:products_list')

    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment', '')
        try:
            rating = int(rating)
            if rating < 1 or rating > 5:
                raise ValueError
        except (ValueError, TypeError):
            return render(request, 'eCommerce/review_product.html', {'product': product, 'error': 'Rating must be a number between 1 and 5.'})

        Review.objects.create(product=product, user=request.user, rating=rating, comment=comment)
        return HttpResponseRedirect(reverse('eCommerce:product_detail', kwargs={'product_id': product.id}))

    return render(request, 'eCommerce/review_product.html', {
        'product': product,
        'is_vendor': is_vendor(request.user),
        'is_buyer': is_buyer(request.user),
    })


@login_required(login_url='/')
def add_item_to_cart(request):
    """Add a selected product quantity to the buyer's session cart."""
    if not is_buyer(request.user):
        return redirect('eCommerce:products_list')

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


@login_required(login_url='/')
def show_user_cart(request):
    """Render the buyer cart page with item totals."""
    if not is_buyer(request.user):
        return redirect('eCommerce:products_list')

    cart_items = cart_items_from_session(request)
    total_price = sum(item['subtotal'] for item in cart_items)
    return render(request, 'eCommerce/main_cart_page.html', {
        'cart': cart_items,
        'total_price': total_price,
        'is_vendor': is_vendor(request.user),
        'is_buyer': is_buyer(request.user),
    })


@login_required(login_url='/')
def checkout(request):
    """Create an order from cart items and clear the cart on success."""
    if not is_buyer(request.user):
        return redirect('eCommerce:products_list')

    cart_items = cart_items_from_session(request)
    if not cart_items:
        return render(request, 'eCommerce/main_cart_page.html', {
            'cart': [],
            'total_price': 0,
            'error': 'Your cart is empty.',
            'is_vendor': is_vendor(request.user),
            'is_buyer': is_buyer(request.user),
        })

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
                    'is_vendor': is_vendor(request.user),
                    'is_buyer': is_buyer(request.user),
                })
            price = product.price
            OrderItem.objects.create(order=order, product=product, quantity=quantity, price=price)
            total_price += price * quantity
            product.stock -= quantity
            product.save()

        order.total_price = total_price
        order.save()
        send_order_email(order)
        request.session['cart'] = {}
        request.session.modified = True

        return render(request, 'eCommerce/checkout_success.html', {'order': order})

    return render(request, 'eCommerce/checkout.html', {
        'cart': cart_items,
        'total_price': sum(item['subtotal'] for item in cart_items),
        'is_vendor': is_vendor(request.user),
        'is_buyer': is_buyer(request.user),
    })


def send_order_email(order):
    """Send an invoice email to the buyer for a completed order."""
    lines = [f'Invoice for Order #{order.pk}', f'Customer: {order.user.username}', '']
    for item in order.items.all():
        lines.append(f'- {item.product.name} x {item.quantity} @ ${item.price} = ${item.price * item.quantity}')
    lines.append('')
    lines.append(f'Total: ${order.total_price}')
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


@login_required(login_url='/')
def clear_cart(request):
    """Clear all items from the buyer's session cart."""
    if not is_buyer(request.user):
        return redirect('eCommerce:products_list')

    request.session['cart'] = {}
    request.session.modified = True
    return redirect('eCommerce:main_cart_page')


@login_required(login_url='/')
def list_stores(request):
    """List stores owned by the current vendor."""
    if not is_vendor(request.user):
        return redirect('grabsomore:welcome')
    stores = user_stores(request.user)
    return render(request, 'eCommerce/stores_list.html', {'stores': stores})


@login_required(login_url='/')
def create_store(request):
    """Create a new store for the current vendor."""
    if not is_vendor(request.user):
        return redirect('grabsomore:welcome')

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        description = request.POST.get('description', '').strip()
        if not name:
            return render(request, 'eCommerce/store_form.html', {'error': 'Store name is required.'})
        Store.objects.create(owner=request.user, name=name, description=description)
        return redirect('eCommerce:stores_list')

    return render(request, 'eCommerce/store_form.html')


@login_required(login_url='/')
def edit_store(request, store_id):
    """Edit an existing store owned by the current vendor."""
    if not is_vendor(request.user):
        return redirect('grabsomore:welcome')
    store = get_object_or_404(Store, pk=store_id, owner=request.user)

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        description = request.POST.get('description', '').strip()
        if not name:
            return render(request, 'eCommerce/store_form.html', {'store': store, 'error': 'Store name is required.'})
        store.name = name
        store.description = description
        store.save()
        return redirect('eCommerce:stores_list')

    return render(request, 'eCommerce/store_form.html', {'store': store})


@login_required(login_url='/')
def delete_store(request, store_id):
    """Delete a store owned by the current vendor."""
    if not is_vendor(request.user):
        return redirect('grabsomore:welcome')
    store = get_object_or_404(Store, pk=store_id, owner=request.user)

    if request.method == 'POST':
        store.delete()
        return redirect('eCommerce:stores_list')

    return render(request, 'eCommerce/store_confirm_delete.html', {'store': store})
