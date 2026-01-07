from decimal import Decimal
from time import timezone
from django.conf import settings
from django.shortcuts import get_object_or_404

from .models import GuestCart, GuestCartItem


SESSION_KEY = 'guest_cart_v1'
GUEST_TOKEN_COOKIE = 'guest_cart_token'

class SessionCart:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        self.data = self.session.get(SESSION_KEY, {})

    def save(self):
        self.session[SESSION_KEY] = self.data
        self.session.modified = True

    def add(self, product, quantity=1, replace=False):
        pid = str(product.pk)
        price = str(product.price)
        if pid in self.data:
            if replace:
                self.data[pid]['quantity'] = int(quantity)
            else:
                self.data[pid]['quantity'] = int(self.data[pid]['quantity']) + int(quantity)
        else:
            self.data[pid] = {'name': product.name, 'unit_price': price, 'quantity': int(quantity)}
        self.save()

    def update(self, product, quantity):
        pid = str(product.pk)
        if pid in self.data:
            if int(quantity) <= 0:
                del self.data[pid]
            else:
                self.data[pid]['quantity'] = int(quantity)
            self.save()

    def remove(self, product):
        pid = str(product.pk)
        if pid in self.data:
            del self.data[pid]
            self.save()

    def clear(self):
        self.data = {}
        self.save()

    def items(self):
        for pid, info in self.data.items():
            yield {
                'product_id': int(pid),
                'name': info['name'],
                'unit_price': Decimal(info['unit_price']),
                'quantity': int(info['quantity']),
                'line_total': Decimal(info['unit_price']) * int(info['quantity']),
            }

    def subtotal(self):
        total = Decimal('0.00')
        for it in self.items():
            total += it['line_total']
        return total

    # Optional: persist to DB GuestCart if models available
    def persist_to_db(self):
        if GuestCart is None:
            return None
        # ensure cookie token
        token = self.request.COOKIES.get(GUEST_TOKEN_COOKIE)
        if not token:
            token = uuid_str = str(uuid4())[:32]
        else:
            uuid_str = token
        cart, _ = GuestCart.objects.get_or_create(token=uuid_str)
        # merge session items into DB

        for it in self.items():
            obj, created = GuestCartItem.objects.get_or_create(
                cart=cart,
                product_id=it['product_id'],
                defaults={'product_name': it['name'], 'unit_price': it['unit_price'], 'quantity': it['quantity']}
            )
            if not created:
                obj.quantity += it['quantity']
                obj.save()
            # set cookie on response externally
        return cart, uuid_str





