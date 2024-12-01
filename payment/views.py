from decimal import Decimal

from django.db.models.expressions import result
from yookassa import Configuration, Payment
from django.conf import settings
from django.shortcuts import render, redirect, reverse, get_object_or_404
from orders.models import Order

# создать экземпляр Stripe
Configuration.account_id = settings.YOOKASSA_TEST_SHOP_ID
Configuration.secret_key = settings.YOOKASSA_TEST_SECRET_KEY

def payment_process(request):
    order_id = request.session.get('order_id', None)
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        # URL для успешной и отмененной оплаты
        result_url = request.build_absolute_uri(reverse('shop:product_list'))
        # Данные для платежа
        payment_data = {
            "amount": {
                "value": f"{order.get_total_cost():.2f}",  # Сумма платежа
                "currency": "RUB"
            },
            "confirmation": {
                "type": "redirect",  # Перенаправление на страницу оплаты
                "return_url": result_url
            },
            "capture": True,  # Автоматическое подтверждение
            "description": f"Order #{order.id}",
            "metadata": {
                "order_id": order.id  # Можно сохранить ID заказа для обработки
            }
        }
        #Создание платежа через ЮKassa
        try:
            payment = Payment.create(payment_data)
            # Перенаправление пользователя на страницу оплаты
            return redirect(payment.confirmation.confirmation_url)
        except Exception as e:
            # Обработка ошибок
            return render(request, 'payment/error.html', {'error': str(e)})
    else:
        return render(request, 'payment/process.html', {'order': order })





