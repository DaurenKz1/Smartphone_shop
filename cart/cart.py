from decimal import Decimal
from django.conf import settings
from store.models import Smartphone


class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, smartphone):
        smartphone_id = str(smartphone.id)
        if smartphone_id not in self.cart:
            self.cart[smartphone_id] = {'quantity': 0, 'price': str(smartphone.price)}
            self.cart[smartphone_id]['quantity'] = 1
        else:
            if self.cart[smartphone_id]['quantity'] < 10:
                self.cart[smartphone_id]['quantity'] += 1

        self.save()

    def update(self, smartphone, quantity):
        smartphone_id = str(smartphone.id)
        self.cart[smartphone_id]['quantity'] = quantity

        self.save()

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, smartphone):
        smartphone_id = str(smartphone.id)
        if smartphone_id in self.cart:
            del self.cart[smartphone_id]
            self.save()

    def __iter__(self):
        smartphone_ids = self.cart.keys()
        smartphones = Smartphone.objects.filter(id__in=smartphone_ids)
        for smartphone in smartphones:
            self.cart[str(smartphone.id)]['smartphone'] = smartphone

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True

