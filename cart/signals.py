from django.contrib.auth.signals import user_logged_out
from django.dispatch import receiver
from .cart import Cart
from .models import UserCart

from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .cart import Cart
from .models import UserCart


@receiver(user_logged_in)
def merge_cart_on_login(sender, request, user, **kwargs):
    cart = Cart(request)

    # Если пользователь имеет корзину в базе данных, объединим ее с сессионной корзиной
    user_cart, _ = UserCart.objects.get_or_create(user=user)

    # Переносим товары из базы в сессию, если они есть
    for product_id, item in user_cart.items.items():
        if product_id in cart.cart:
            cart.cart[product_id]['quantity'] += item['quantity']
        else:
            cart.cart[product_id] = item
    cart.save()  # Сохраняем изменения в сессии и базе данных
    cart.save_user_cart()


@receiver(user_logged_out)
def save_cart_on_logout(sender, request, user, **kwargs):
    if user.is_authenticated:
        cart = Cart(request)
        # Если в корзине пользователя есть товары, сохраняем их в UserCart
        if cart.cart:
            # Сохранить корзину в базе данных
            user_cart, _ = UserCart.objects.get_or_create(user=user)
            user_cart.items = cart.cart  # Сохраняем текущие товары из сессии
            user_cart.save()
        # Очистить корзину в сессии после выхода
        cart.clear()
