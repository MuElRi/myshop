from itertools import product
from statistics import quantiles

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm

#  @require_POST
# def cart_update_cart(request):
#     cart = Cart(request)
#     product = get_object_or_404(Product, id=product_id)
#     form = CartAddProductForm(request.POST)
#     if form.is_valid():
#         cd = form.cleaned_data
#         cart.add(quantity=cd['quantity'],
#                  product=cd['product_id'])
#         return redirect('cart:cart_detail')

# @require_POST
# def cart_remove(request, product_id):
#     cart = Cart(request)
#     product = get_object_or_404(Product, id=product_id)
#     cart.remove(product)
#     return redirect('cart:cart_detail')

def cart_detail(request):
    cart = Cart(request)
    quantities = {}
    for item in cart:
        product = item['product']
        item['update_quantity_form'] = CartAddProductForm(initial={
                                        'quantity': item['quantity'],
                                        'action_type': 'update-cart',
                                        'product_id': product.id,
                                        })
        quantities[product.id] = item['quantity']
    return render(request, 'cart/detail.html', {'cart': cart,
                                                'quantities': quantities})
# @require_POST
# def add_to_cart(request):
#     product_id = request.POST.get('id')
#     action = request.POST.get('action')
#     if product_id and action:
#         try:
#             product = Product.objects.get(id=product_id)
#             cart = Cart(request)
#             if action == 'add':
#                 cart.add(product=product)
#                 print(cart.cart)
#             else:
#                 print(cart.cart)
#                 cart.remove(product=product)
#             return JsonResponse({'status': "ok"})
#         except Product.DoesNotExist:
#             return JsonResponse({'status': "error"})
#     return JsonResponse({'status': "error"})



@require_POST
def cart_add(request):
    print(request.POST)
    form = CartAddProductForm(request.POST)

    if form.is_valid():
        cd = form.cleaned_data
        product_id = cd["product_id"]
        action = cd["action_type"]
        #Добавление продукта в корзину
        if action == "add":
            quantity = 1
            action = "update"
        #Обновление количества продукта в корзине
        else:
            quantity = cd['quantity']

        try:
            cart = Cart(request)
            product = Product.objects.get(id=product_id)
            # Если нужно удалить продукт со СТРАНИЦЫ корзины
            if action == "update-cart" and quantity == 0:
                cart.remove(product)
                return HttpResponse('')
            # Если нужно добавить продукт в корзину
            # или обновить его количество,
            # или удалить его оттуда
            else:
                if quantity == 0:
                    cart.remove(product)
                    action = "add"
                else:
                    cart.add(product, quantity)
                form = CartAddProductForm(initial={
                    'quantity': quantity,
                    'action_type': action,
                    'product_id': product_id})
        except Product.DoesNotExist:
            pass
    return render(request, "shop/form_add.html",
                  {"cart_product_form": form, "quantity": quantity})


