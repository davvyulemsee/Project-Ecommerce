# app: cart/views.py
from decimal import Decimal
from itertools import count

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST
from .session_cart import SessionCart
from catalog.models import Product
from daraja import Mpesa
from django_daraja.mpesa.core import MpesaClient
  # replace with your actual product model

@require_POST
def add_to_cart(request, product_pk):
    product = get_object_or_404(Product, pk=product_pk)
    try:
        qty = int(request.POST.get('quantity', 1))
    except (TypeError, ValueError):
        return HttpResponseBadRequest("Invalid quantity")
    if qty <= 0:
        return HttpResponseBadRequest("Quantity must be positive")
    sc = SessionCart(request)
    sc.add(product, quantity=qty)
    # return JSON for JS updates, otherwise redirect
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        total_items = sum(i['quantity'] for i in sc.items())
        return JsonResponse({'items_count': total_items, 'subtotal': str(sc.subtotal())})
    return redirect('cart:detail')

def cart_detail(request):
    sc = SessionCart(request)
    raw_items = list(sc.items())
    subtotal = sc.subtotal()

    pids = [it['product_id'] for it in raw_items]
    # Bulk fetch products that still exist
    products = Product.objects.filter(pk__in=pids).only('id', 'name', 'image', 'price')
    prod_map = {p.pk: p for p in products}

    items = []
    for it in raw_items:
        pid = it['product_id']
        product = prod_map.get(pid)
        image_url = None
        if product and getattr(product, 'image', None):
            try:
                image_url = product.image.url
            except Exception:
                image_url = None

        items.append({
            'product_id': pid,
            'name': it.get('name') or (product.name if product else ''),
            'unit_price': it.get('unit_price'),
            'quantity': it.get('quantity'),
            'line_total': it.get('line_total'),
            'image_url': image_url,
            # optional: include product instance if you want to reference other fields in template
            # 'product': product,
        })

    return render(request, 'cart/detail.html', {'items': items, 'subtotal': subtotal})

@require_POST
def update_cart_item(request, product_pk):
    product = get_object_or_404(Product, pk=product_pk)
    try:
        qty = int(request.POST.get('quantity', 0))
    except (TypeError, ValueError):
        return HttpResponseBadRequest("Invalid quantity")
    sc = SessionCart(request)
    sc.update(product, qty)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'items_count': sum(i['quantity'] for i in sc.items()), 'subtotal': str(sc.subtotal())})
    return redirect('cart:detail')

@require_POST
def remove_cart_item(request, product_pk):
    product = get_object_or_404(Product, pk=product_pk)
    sc = SessionCart(request)
    sc.remove(product)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'items_count': sum(i['quantity'] for i in sc.items()), 'subtotal': str(sc.subtotal())})
    return redirect('cart:detail')

def checkout(request):
    sc = SessionCart(request)
    subtotal = sc.subtotal()
    items = sum(1 for _ in sc.items())

    return render(request, 'cart/checkout.html', {'subtotal':subtotal, 'items':items})

def pay_mpesa(request):
    sc = SessionCart(request)
    subtotal = sc.subtotal()
    if request.method == 'POST':
        phone = request.POST['phone']
        amount = subtotal
        transaction_desc = 'Products payment'

        cl = MpesaClient()

        response = cl.stk_push(
            phone_number = phone,
            amount = amount,
            transaction_desc=transaction_desc,
        )

        return JsonResponse(response)