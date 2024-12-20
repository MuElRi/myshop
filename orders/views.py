from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
import weasyprint
from .models import Order, OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from .tasks import order_created
from django.urls import reverse_lazy
from django.views.generic import *

class OrderCreateView(FormView):
    form_class = OrderCreateForm
    success_url = reverse_lazy('payment:process')
    template_name = 'orders/order/create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = Cart(self.request)
        return context

    def form_valid(self, form):
        order = form.save(commit=True)
        cart = Cart(self.request)

        order = self._create_order(order, cart)
        self._create_item_order(order, cart)

        cart.clear(only_session=False)
        order_created.delay(order.id)
        self.request.session['order_id'] = order.id
        return super().form_valid(form)

    def _create_order(self, order, cart):
        if cart.coupon:
            order.coupon = cart.coupon
            order.discount = cart.coupon.discount
        if self.request.user.is_authenticated:
            order.user = self.request.user
        order.save()
        return order

    def _create_item_order(self, order, cart):
        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                price=item['price'],
                quantity=item['quantity']
            )


class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'orders/order_list.html'
    context_object_name = 'orders'

    def get_queryset(self, queryset=None):
        orders = super().get_queryset()
        return orders.filter(user = self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        orders = context['orders']
        paid_orders = orders.filter(paid=True)
        context['total_spent'] = sum(order.get_total_cost() for order in paid_orders)
        context['paid_orders'] = paid_orders
        return context


class OrderStatusView(DetailView):
    model = Order
    context_object_name = 'order'
    template_name = 'orders/order/created.html'

    def get_object(self, queryset=None):
        order_pk = self.request.session.get('order_id', None)
        order = get_object_or_404(Order, id=order_pk)
        return order


class StaffMemberRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff


class AdminOrderDetailView(StaffMemberRequiredMixin, DetailView):
    model = Order
    template_name = 'admin/orders/order/detail.html'
    context_object_name = 'order'


class AdminOrderPDFView(StaffMemberRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        order = get_object_or_404(Order, id=self.kwargs['pk'])
        html = render_to_string('orders/order/pdf.html',{'order': order})
        response = self._generate_pdf(order, html)
        return response

    def _generate_pdf(self, order, html):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'filename=order_{order.id}.pdf'
        stylesheets = [weasyprint.CSS(settings.STATIC_ROOT / 'shop/css/pdf.css')]
        weasyprint.HTML(string=html).write_pdf(response, stylesheets=stylesheets)
        return response


# @staff_member_required
# def admin_order_pdf(request, order_id):
#     order = get_object_or_404(Order, id=order_id)
#     html = render_to_string('orders/order/pdf.html',
#                             {'order': order})
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = f'filename=order_{order.id}.pdf'
#     weasyprint.HTML(string=html).write_pdf(
#         response,
#         stylesheets=[weasyprint.CSS(
#         settings.STATIC_ROOT / 'shop/css/pdf.css')]
#     )
#     return response





# @staff_member_required
# def admin_order_detail(request, order_id):
#     order = get_object_or_404(Order, id=order_id)
#     return render(request,
#                   'admin/orders/order/detail.html',
#                   {'order': order})



# def order_create(request):
#     cart = Cart(request)
#     if request.method == 'POST':
#         form = OrderCreateForm(request.POST)
#         if form.is_valid():
#             order = form.save(commit=False)
#             if cart.coupon:
#                 order.coupon = cart.coupon
#                 order.discount = cart.coupon.discount
#             order.save()
#             for item in cart:
#                 OrderItem.objects.create(order=order, product=item['product'],
#                                          price=item['price'], quantity=item['quantity'])
#             if request.user.is_authenticated:
#                 order.user = request.user
#                 order.save()
#
#             cart.clear(only_session=False)
#             #Запустить асинхронное задание
#             order_created.delay(order.id)
#             request.session['order_id'] = order.id
#             return redirect(reverse('payment:process'))
#     else:
#         form = OrderCreateForm()
#     return render(request, 'orders/order/create.html',
#                     {'cart': cart, 'form': form})


# def order_status(request):
#     order_id = request.session.get('order_id', None)
#     order = get_object_or_404(Order, id=order_id)
#     return render(request, 'orders/order/created.html',
#                   {'order': order})



# @login_required
# def order_list(request):
#     orders = request.user.orders.all()
#     paid_orders = orders.filter(paid=True)
#     total_spent = sum(order.get_total_cost() for order in paid_orders)
#
#     return render(request, 'orders/order_list.html',
#                   {'orders': orders, 'paid_orders': paid_orders,
#                    'total_spent': total_spent})
