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
    subject = f'Номер заказа: {order.id}'
    message = (f'Успешно!\n\n'
               f'Ваш заказ: {order.id}')
    mail_sent = send_mail(subject, message, 'eldar00319g@gmail.com', [order.email])
    return mail_sent