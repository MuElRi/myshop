from decimal import Decimal
from django.conf import settings
from shop.models import Product

class Cart:

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # сохранить пустую корзину в сеансе
            cart = self.session[settings.CART_SESSION_ID] = {}
        self._cart = cart

    def add(self, product, quantity = 1):
        """Добавить товар в корзину или обновить его кол-во"""
        product_id = str(product.id)
        self._cart[product_id] = {'quantity': quantity, 'price': str(product.price)}
        self.save()

    def save(self):
        #пометить сеанс как измененный, чтобы обеспечить его сохранение
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self._cart:
            del self._cart[product_id]
            self.save()

    def __iter__(self):
        """Прокрутить товарные позиции корзины в цикле и получить товары из базы данных"""
        product_ids = self._cart.keys()
        # получить объекты product и добавить их в корзину
        products = Product.objects.filter(id__in=product_ids)
        _cart = self._cart.copy()
        for product in products:
            _cart[str(product.id)]['product'] = product
        for item in _cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """Подсчитать все товарные позиции в корзине"""
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self._cart.values())

    def clear(self):
        """Удалить корзину из сеанса"""
        del self.session[settings.CART_SESSION_ID]
        self.save()

    @property
    def cart(self):
        return self._cart


