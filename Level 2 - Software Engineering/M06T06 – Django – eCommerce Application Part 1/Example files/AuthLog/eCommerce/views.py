from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.conf import settings
from .models import Product, Order, OrderItem, Review


def is_vendor(user):
    return user.is_authenticated and user.groups.filter(name='Vendors').exists()


def cart_items_from_session(request):
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
    products = Product.objects.all()
    return render(request, 'eCommerce/products_list.html', {
        'products': products,
        'is_vendor': is_vendor(request.user),
    })


def view_product_page(request):
    if request.method == 'POST':
        product_name = request.POST.get('product')
        if not product_name:
            return render(request, 'eCommerce/product_page.html', {'error': 'Please enter a product name.'})
        try:
            product = Product.objects.get(name__icontains=product_name)
            return render(request, 'eCommerce/product_page.html', {'product': product})
        except Product.DoesNotExist:
            return render(request, 'eCommerce/product_page.html', {'error': 'Product not found.'})
    return render(request, 'eCommerce/product_page.html')


def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    reviews = product.reviews.all()
    return render(request, 'eCommerce/product_detail.html', {
        'product': product,
        'reviews': reviews,
        'is_vendor': is_vendor(request.user),
    })


@login_required(login_url='/')
def add_product(request):
    if not is_vendor(request.user):
        return render(request, 'eCommerce/add_product.html', {'error': 'Only vendors can add products.'})

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        price = request.POST.get('price')
        stock = request.POST.get('stock')

        if not name or not price or not stock:
            return render(request, 'eCommerce/add_product.html', {'error': 'Name, price, and stock are required.'})

        try:
            price = float(price)
            stock = int(stock)
        except ValueError:
            return render(request, 'eCommerce/add_product.html', {'error': 'Price and stock must be valid numbers.'})

        Product.objects.create(vendor=request.user, name=name, description=description, price=price, stock=stock)
        return HttpResponseRedirect(reverse('eCommerce:products_list'))

    return render(request, 'eCommerce/add_product.html')


@login_required(login_url='/')
def edit_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if product.vendor != request.user:
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
    product = get_object_or_404(Product, pk=product_id)
    if product.vendor != request.user:
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

    return render(request, 'eCommerce/review_product.html', {'product': product})


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
        return render(request, 'eCommerce/main_cart_page.html', {'cart': [], 'total_price': 0, 'error': 'Your cart is empty.'})

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

    return render(request, 'eCommerce/checkout.html', {'cart': cart_items, 'total_price': sum(item['subtotal'] for item in cart_items)})


def send_order_email(order):
    lines = [f'Invoice for Order #{order.pk}', f'Customer: {order.user.username}', '']
    for item in order.items.all():
        lines.append(f'- {item.product.name} x {item.quantity} @ R{item.price} = R{item.price * item.quantity}')
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
