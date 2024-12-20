from celery.worker.control import active
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.views.generic import FormView

from .models import Coupon
from .forms import CouponApplyForm


class CouponApplyView(FormView):
    form_class = CouponApplyForm
    http_method_names = ['post']
    success_url = reverse_lazy('cart:cart_detail')

    def form_valid(self, form):
        now = timezone.now()
        code = form.cleaned_data['code']
        try:
            coupon = Coupon.objects.get(code__iexact=code,
                                        valid_form__lte=now,
                                        valid_to__gte=now,
                                        active=True)
            self.request.session['coupon_id'] = coupon.id
        except Coupon.DoesNotExist:
            self.request.session['coupon_id'] = None
        return super().form_valid(form)