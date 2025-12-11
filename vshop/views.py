from django.shortcuts import render
from .models import Product
from django.shortcuts import get_object_or_404, redirect
from .models import Product, Cart, CartItem
from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Order, Product, Category, Transaction
from django.views.decorators.http import require_POST
from django.contrib import messages
import random




def home(request):
    products = Product.objects.all()[:8]
    categories = Category.objects.all()
    cart_items_count = request.session.get('cart_items_count', 0)
    return render(request, 'home.html', {
        'products': products,
        'categories': categories,
        'cart_items_count': cart_items_count
    })
# Create your views here.

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    request.session['cart_id'] = cart.id
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    return redirect('cart_detail')

@login_required
def cart_detail(request):
    
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.cart_items.all()
    
    total = sum([item.subtotal  for item in items])
    created_at = cart.created_at

    context = {
        'cart': cart,
        'items': items,
        'total':total,
        'created_at': created_at,
        
    }
    return render(request, 'cart_detail.html', context)

@login_required(login_url='login')
def checkout(request):
    cart_id = request.session.get('cart_id')

    if not cart_id:
        return redirect('cart_detail')

    try:
        cart = Cart.objects.get(id=cart_id)
    except Cart.DoesNotExist:
        return redirect('cart_detail')

    # Create ORDER
    order = Order.objects.create(
        user=request.user,
        cart=cart,
        total=cart.get_total(),   # adjust if needed
        status="Success"          # Payment is mocked
    )

    # Clear Cart after successful payment
    cart.items.all().delete()
    request.session['cart_id'] = None

    # Redirect user to payment success page
    return redirect('payment_success', order_id=order.id)


@login_required
def success(request):
    cart_id = request.session.get('cart_id')
    if cart_id:
        cart = Cart.objects.get(id=cart_id)
        Order.objects.create(
            user=request.user,
            cart=cart,
            total_amount=cart.total,
            stripe_payment_intent='PAID'  # for simplicity, real app uses Stripe ID
        )
        del request.session['cart_id']
    return render(request, 'success.html')

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'order_history.html', {'orders': orders})


@login_required
@require_POST
def update_cart(request):
    item_id = request.POST.get('increment') or request.POST.get('decrement') or request.POST.get('remove')
    if item_id:
        cart_item = get_object_or_404(CartItem, id=item_id)
        if 'increment' in request.POST:
            cart_item.quantity += 1
            cart_item.save()
        elif 'decrement' in request.POST:
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
            else:
                cart_item.delete()
        elif 'remove' in request.POST:
            cart_item.delete()

    return redirect('cart_detail')

def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

def category_products(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)
    return render(request, 'category_product.html', {'category': category, 'products': products})


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product_detail.html', {'product': product})



def home(request):
    products = Product.objects.all()[:8]
    categories = Category.objects.all()
    cart_items_count = request.session.get('cart_items_count', 0)
    return render(request, 'home.html', {
        'products': products,
        'categories': categories,
        'cart_items_count': cart_items_count
    })
    
@login_required
def payment(request, order_id):
    order = Order.objects.get(id=order_id, user=request.user)
    
    # Create a dummy transaction
    transaction = Transaction.objects.create(user=request.user, order=order, amount=order.total_amount)
    
    return render(request, 'payment_gateway.html', {'order': order, 'transaction': transaction})

@login_required(login_url='login')
def payment_process(request):
    cart_id = request.session.get('cart_id')

    if not cart_id:
        return redirect('cart_detail')

    cart = Cart.objects.get(id=cart_id)

    # Create order
    order = Order.objects.create(
        user=request.user,
        cart=cart,
        total_amount=cart.total,
        status="pending"
    )

    # Fake payment result
    success = True  # Always success for mock

    if success:
        # Create Transaction
        transaction = Transaction.objects.create(
            order=order,
            amount=cart.total,
            user=request.user,
            status="success"
        )

        order.status = "success"
        order.save()

        # Clear cart
        cart.cart_items.all().delete()
        request.session['cart_id'] = None

        return redirect('order_success', order_id=order.id)

    else:
        # Failed payment
        Transaction.objects.create(
            order=order,
            amount=cart.total,
            payment_id=f"TESTPAY-{order.id}",
            status="failed"
        )

        order.status = "failed"
        order.save()

        return redirect('payment_page')

def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'order_success.html', {'order': order})

@login_required(login_url='login')
def proceed_to_checkout(request):
    cart_id = request.session.get('cart_id')

    if not cart_id:
        return redirect('cart_detail')

    cart = Cart.objects.filter(id=cart_id).first()

    if not cart or cart.cart_items.count() == 0:
        return redirect('cart_detail')

    total_amount = cart.total

    # Show payment page (DO NOT create order here)
    return render(request, 'payment.html', {
        'cart': cart,
        'total_amount': total_amount,
    })
    
@login_required(login_url='login')
def payment_page(request):
    cart_id = request.session.get('cart_id')

    if not cart_id:
        return redirect('cart_detail')

    cart = Cart.objects.get(id=cart_id)

    return render(request, 'payment.html', {'cart': cart})

