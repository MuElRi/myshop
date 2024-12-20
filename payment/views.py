from decimal import Decimal
from django.views.generic import ListView, DetailView
from weasyprint.css.validation.properties import order

from shop.recommender import Recommender
from django.db.models.expressions import result
from yookassa import Configuration, Payment
from django.conf import settings
from django.shortcuts import render, redirect, reverse, get_object_or_404
from orders.models import Order

# создать экземпляр Stripe
Configuration.account_id = settings.YOOKASSA_TEST_SHOP_ID
Configuration.secret_key = settings.YOOKASSA_TEST_SECRET_KEY


class PaymentProcessView(DetailView):
    model = order
    template_name = "payment/process.html"

    def get_object(self, queryset=None):
        order_pk = self.request.session.get('order_id', None)
        order = get_object_or_404(Order, id=order_pk)
        return order

    def post(self, request, *args, **kwargs):
        result_url = request.build_absolute_uri(reverse('orders:order_status'))
        order = self.get_object()

        # Создание товарных позиций для чека
        items = []
        products = []
        for item in order.items.all():  # order.items - связь с товарными позициями заказа
            items.append({
                "description": item.product.name,  # Название товара
                "quantity": str(item.quantity),  # Количество (в виде строки)
                "amount": {
                    # Костыль: Цена за единицу товара с учетом скидки
                    "value": f"{item.price * (1 - order.discount / 100):.2f}",
                    "currency": "RUB"
                },
                "vat_code": 1  # Пример: ставка НДС 20%
            })
            products.append(item.product)

        # Сохраняем в рекомендации товары которые покупают вместе
        r = Recommender()
        r.products_bought(products)

        # Данные для платежа
        payment_data = {
            "amount": {
                "value": f"{order.get_total_cost():.2f}",  # Общая сумма заказа
                "currency": "RUB"
            },
            "confirmation": {
                "type": "redirect",  # Перенаправление на страницу оплаты
                "return_url": result_url
            },
            "capture": True,  # Автоматическое подтверждение
            "description": f"Order #{order.id}",
            "metadata": {
                "order_id": order.id  # Сохранение ID заказа для обработки
            },
            "receipt": {
                "customer": {
                    "email": order.email,  # Почта покупателя
                },
                "items": items
            }
        }
        # Создание платежа через ЮKassa
        try:
            payment = Payment.create(payment_data)
            # Перенаправление пользователя на страницу оплаты
            return redirect(payment.confirmation.confirmation_url)
        except Exception as e:
            # Обработка ошибок
            return render(request, 'payment/error.html', {'error': str(e)})



