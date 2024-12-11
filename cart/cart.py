from decimal import Decimal
from django.conf import settings
from shop.models import Product
from .models import UserCart
from coupons.models import Coupon

class Cart:

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # сохранить пустую корзину в сеансе
            cart = self.session[settings.CART_SESSION_ID] = {}
        self._cart = cart
        self.user = request.user if request.user.is_authenticated else None
        self.coupon_id = self.session.get('coupon_id')

    def save_user_cart(self):
        # Сохранить сессионную корзину в базу данных
        if self.user:
            user_cart, _ = UserCart.objects.get_or_create(user=self.user)
            if self._cart:
                user_cart.items = self._cart
            else:
                user_cart.items = {}
            user_cart.save()

    def save(self):
        self.session.modified = True

    def increase(self, product, limit=20):
        product_id = str(product.id)
        if product_id not in self._cart.keys():
            self._cart[product_id] = {'quantity': 1, 'price': str(product.price)}
        else:
            if self._cart[product_id]['quantity']<limit:
                self._cart[product_id]['quantity'] += 1
        self.save()
        self.save_user_cart()

    def reduce(self, product):
        product_id = str(product.id)
        if product_id in self._cart.keys():
            if self._cart[product_id]['quantity'] > 1:
                self._cart[product_id]['quantity'] -= 1
            else:
                self.remove(product)
        self.save()
        self.save_user_cart()

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self._cart:
            del self._cart[product_id]
            self.save()
            self.save_user_cart()

    def get_quantity(self, product):
        product_id = str(product.id)
        if product_id in self._cart.keys():
            return self._cart[product_id]["quantity"]
        return 0

    def __iter__(self):
        """Прокрутить товарные позиции корзины в цикле и получить товары из базы данных"""
        product_ids = self._cart.keys()
        # получить объекты product и добавить их в корзину
        products = Product.objects.filter(id__in=product_ids)
        _cart = self._cart.copy()
        for product in products:
            _cart[str(product.id)]['product'] = product
        for item in _cart.values():
            item['price'] = int(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """Подсчитать все товарные позиции в корзине"""
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_product_price(self, product):
        product_id = str(product.id)
        if product_id in self._cart.keys():
            quantity = self._cart[product_id]["quantity"]
            price = int(self._cart[product_id]["price"])
            return quantity*price
        return 0


    def get_total_price(self):
        return sum(int(item['price']) * item['quantity'] for item in self._cart.values())


    def clear(self, only_session=True):
        """Удалить корзину из сеанса и базы данных"""
        del self.session[settings.CART_SESSION_ID]
        self.save()
        if not only_session:
            self._cart = None
            self.save_user_cart()

    @property
    def cart(self):
        return self._cart


    @property
    def coupon(self):
        if self.coupon_id:
            try:
                return Coupon.objects.get(id=self.coupon_id)
            except Coupon.DoesNotExist:
                pass
        return None

    def get_discount(self):
        if self.coupon:
            return int((self.coupon.discount / 100) * self.get_total_price())
        return 0

    def get_total_price_after_discount(self):
        return self.get_total_price() - self.get_discount()