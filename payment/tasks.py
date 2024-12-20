from io import BytesIO
from celery import shared_task
import weasyprint
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from orders.models import Order

@shared_task
def payment_completed(order_id):
    """
    Задание по отправке уведомления по электронной почте
    при успешной оплате заказа.
    """
    order = Order.objects.get(id=order_id)
    # create invoice e-mail
    subject = f'My Shop – счет №{order.id}'
    message = 'Пожалуйста, ознакомьтесь.'
    email = EmailMessage(subject,
                         message,
                         'eldar00319g@gmail.com',
                         [order.email])
    # сгенерировать PDF
    html = render_to_string('orders/order/pdf.html', {'order': order})
    out = BytesIO()
    stylesheets=[weasyprint.CSS(settings.STATIC_ROOT / 'shop/css/pdf.css')]
    weasyprint.HTML(string=html).write_pdf(out, stylesheets=stylesheets)
    # прикрепить PDF-файл
    email.attach(f'order_{order.id}.pdf',
                 out.getvalue(),
                 'application/pdf')

    email.send()