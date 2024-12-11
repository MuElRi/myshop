import json
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from yookassa import Configuration, Payment
from orders.models import Order
from ..tasks import payment_completed

# Настройка API ЮKassa
Configuration.account_id = settings.YOOKASSA_TEST_SHOP_ID
Configuration.secret_key = settings.YOOKASSA_TEST_SECRET_KEY


@csrf_exempt
def payment_webhook(request):
    if request.method == "POST":
        try:
            # Получение данных из запроса
            event_data = json.loads(request.body)
            # Проверка типа уведомления
            if event_data.get('event') == 'payment.succeeded':
                payment_id = event_data['object']['id']
                # Получаем данные платежа
                payment = Payment.find_one(payment_id)
                # Логика обработки успешного платежа
                order_id = payment.metadata.get('order_id')
                # Обновляем статус заказа
                order = Order.objects.get(id=order_id)
                order.paid = True
                order.payment_id = payment_id
                order.save()
                payment_completed.delay(order.id)
                print(f"Оплата успешна для заказа {order_id}")

            elif event_data.get('event') == 'payment.canceled':
                payment_id = event_data['object']['id']
                # Логика обработки отменённого платежа
                order_id = event_data['object']['metadata']['order_id']
                # Пример: Order.objects.filter(id=order_id).update(status='canceled')
                print(f"Оплата отменена для заказа {order_id}")
            return HttpResponse(status=200)

        except Exception as e:
            print(f"Ошибка обработки вебхука: {e}")
            return HttpResponse(status=400)
    else:
        return HttpResponse(status=405)
