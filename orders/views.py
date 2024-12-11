from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
import weasyprint
from .models import Order, OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from .tasks import order_created
from django.urls import reverse

def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'],
                                         price=item['price'], quantity=item['quantity'])
            if request.user.is_authenticated:
                order.user = request.user
                order.save()

            cart.clear(only_session=False)
            #Запустить асинхронное задание
            order_created.delay(order.id)
            request.session['order_id'] = order.id
            return redirect(reverse('payment:process'))
    else:
        form = OrderCreateForm()
    return render(request, 'orders/order/create.html',
                    {'cart': cart, 'form': form})

from django.shortcuts import get_object_or_404, render
from .models import Order

def order_status(request):
    order_id = request.session.get('order_id', None)
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'orders/order/created.html',
                  {'order': order})

@login_required
def order_list(request):
    orders = request.user.orders.all()
    paid_orders = orders.filter(paid=True)
    total_spent = sum(order.get_total_cost() for order in paid_orders)

    return render(request, 'orders/order_list.html',
                  {'orders': orders, 'paid_orders': paid_orders,
                   'total_spent': total_spent})

@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request,
                  'admin/orders/order/detail.html',
                  {'order': order})

@staff_member_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string('orders/order/pdf.html',
                            {'order': order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order_{order.id}.pdf'
    weasyprint.HTML(string=html).write_pdf(response,
                                           stylesheets=[weasyprint.CSS(
                                               settings.STATIC_ROOT / 'shop/css/pdf.css')])
    return response
