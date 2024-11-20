from statistics import quantiles

from django.contrib.admin import action
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST

from .models import Category, Product
from cart.forms import CartAddProductForm
from cart.cart import Cart


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    cart = Cart(request)
    cart_ = cart.cart

    forms = {}
    quantities = {}
    for product in products:
        if str(product.id) in cart_:
            quantity = cart_[str(product.id)]['quantity']
            action = "update"
        else:
            quantity = 0
            action = "add"

        forms[product.id] = CartAddProductForm(initial={
            "quantity": quantity,
            "action_type": action,
            "product_id": product.id})
        quantities[product.id] = quantity
    print(forms)
    print(quantities)

    return render(request, 'shop/product/list.html',
                  {'category': category, 'categories': categories, 'quantities': quantities,
                            'products': products, 'cart_product_forms': forms})

def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart = Cart(request)
    cart_ = cart.cart

    if str(product.id) in cart_:
        quantity = cart_[str(product.id)]['quantity']
        action = "update"
    else:
        quantity = 0
        action = "add"

    form = CartAddProductForm(initial={
        'quantity': quantity,
        "action_type": action,
        "product_id": id})

    return render(request, 'shop/product/detail.html',
        {'product': product, 'cart_product_form': form, 'quantity': quantity})




