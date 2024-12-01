from celery import shared_task
from django.core.mail import send_mail
from .models import Order
import logging


logger = logging.getLogger(__name__)

@shared_task
def order_created(order_id):
    """
    Задание по отправке уведомления по эл почте при успешной соединении заказа.
    """
    order = Order.objects.get(id=order_id)
    subject = f'Order nr. {order.id}'
    message = (f'Успешно!\n\n'
               f'Твой заказ: {order.id}')
    try:
        mail_sent = send_mail(subject, message, 'eldar00319g@gmail.com', [order.email])
        logger.info(f"Письмо для заказа {order_id} отправлено успешно: {mail_sent}")
    except Exception as e:
        logger.error(f"Ошибка при отправке письма для заказа {order_id}: {e}")
    return mail_sent