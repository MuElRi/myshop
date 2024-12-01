from django.shortcuts import render, get_object_or_404
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

    forms = {}
    quantities = {}
    cart = Cart(request)
    for product in products:
        quantity = cart.get_quantity(product)
        forms[product.id] = CartAddProductForm(initial={
            "quantity": quantity,
            "product_id": product.id})
        quantities[product.id] = quantity
    return render(request, 'shop/product/list.html',
                  {'category': category, 'categories': categories, 'quantities': quantities,
                            'products': products, 'cart_product_forms': forms})

def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart = Cart(request)
    quantity = cart.get_quantity(product)
    form = CartAddProductForm(initial={
        'quantity': quantity,
        "product_id": id})
    return render(request, 'shop/product/detail.html',
        {'product': product, 'cart_product_form': form, 'quantity': quantity})




