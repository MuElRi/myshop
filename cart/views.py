from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import UpdateView, FormView, TemplateView
from coupons.forms import CouponApplyForm
from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm
from shop.recommender import Recommender


class CartDetailView(TemplateView):
    template_name = 'cart/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = Cart(self.request)
        quantities = {}
        for item in cart:
            product = item['product']
            quantities[product.id] = item['quantity']
            item['update_quantity_form'] = CartAddProductForm(
                                    initial={
                                        'quantity': item['quantity'],
                                        'product_id': product.id,
                                    })
        coupon_apply_form = CouponApplyForm()
        r = Recommender()
        cart_products = [item['product'] for item in cart]
        if (cart_products):
            recommended_products = r.suggested_products_for(cart_products,
                                                            max_results=4)
        else:
            recommended_products = []

        context['cart'] = cart
        context['quantities'] = quantities
        context['coupon_apply_form'] = coupon_apply_form
        context['recommended_products'] = recommended_products

        return context



class UpdateCartView(FormView):
    form_class = CartAddProductForm
    http_method_names = ['post']

    def form_valid(self, form):
        product_id = form.cleaned_data["product_id"]
        action = self.request.POST.get("action")
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return JsonResponse({"success": False, "message": "Продукт не найден."},
                                status=404)
        cart = Cart(self.request)
        # добавляем 1 товар
        if action == "Add" or action == "+":
            cart.increase(product, limit=20)
        # уменьшаем на 1 количество товара или
        # удаляем его из корзины, если его кол-во равно 0
        elif action == "-":
            cart.reduce(product)

        return JsonResponse({
            "success": True,
            "quantity": cart.get_quantity(product),
            "product_id": product.id,
            "total_price": cart.get_total_price(),
            "total_price_after_discount": cart.get_total_price_after_discount(),
            "total_product_price": cart.get_total_product_price(product),
            "total_items": len(cart),
            "discount": cart.get_discount(),
        })

    def form_invalid(self, form):
        return JsonResponse(
       {"success": False, "message": "Неверные данные формы."},
            status=400
        )








