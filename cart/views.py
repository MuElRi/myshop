from itertools import product
from statistics import quantiles

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm

def cart_detail(request):
    cart = Cart(request)
    quantities = {}
    for item in cart:
        product = item['product']
        item['update_quantity_form'] = CartAddProductForm(initial={
                                        'quantity': item['quantity'],
                                        'product_id': product.id,
                                        })
        quantities[product.id] = item['quantity']
    return render(request, 'cart/detail.html', {'cart': cart,
                                                'quantities': quantities})

@require_POST
def update_cart(request):
    form = CartAddProductForm(request.POST)
    if not form.is_valid():
        return JsonResponse({"success": False, "message": "Неверные данные формы."},
                            status=400)

    product_id = form.cleaned_data["product_id"]
    action = request.POST.get("action")

    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return JsonResponse({"success": False, "message": "Продукт не найден."},
                            status=404)

    cart = Cart(request)
    # добавляем товар с количеством 1
    if action == "Add" or action == "+":
        cart.increase(product, limit=20)
    # уменьшаем количество товара или удаляем его из корзины, если его кол-во равно 0
    elif action == "-":
        cart.reduce(product)

    total_product_price = cart.get_total_product_price(product)
    total_price = cart.get_total_price()
    total_items = len(cart)

    quantity = cart.get_quantity(product)
    return JsonResponse({"success": True, "quantity": quantity,
                         "product_id": product.id, "total_price": total_price,
                         "total_product_price": total_product_price, "total_items": total_items})





