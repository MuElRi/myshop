from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from cart.forms import CartAddProductForm
from cart.cart import Cart
from .forms import PriceFilterForm


# def product_list(request, category_slug=None):
#     category = None
#     categories = Category.objects.all()
#     products = Product.objects.filter(available=True)
#     if category_slug:
#         category = get_object_or_404(Category, slug=category_slug)
#         products = products.filter(category=category)
#
#     chipest_product = products.order_by('price').first()
#     most_expensive_product =  products.order_by('-price').first()
#     price_form = PriceFilterForm(initial={
#         'min_price': chipest_product.price,
#         'max_price': most_expensive_product.price,
#     })
#
#     cart_product_forms = {}
#     quantities = {}
#     cart = Cart(request)
#     for product in products:
#         quantity = cart.get_quantity(product)
#         cart_product_forms[product.id] = CartAddProductForm(initial={
#             "quantity": quantity,
#             "product_id": product.id})
#         quantities[product.id] = quantity
#     return render(request, 'shop/product/list.html',
#                   {'category': category, 'categories': categories, 'quantities': quantities,
#                             'products': products, 'price_form': price_form, 'cart_product_forms': cart_product_forms})

#  def product_list(request, category_slug=None):
#      category = None
#      categories = Category.objects.all()
#      products = Product.objects.filter(available=True)
#      if category_slug:
#          category = get_object_or_404(Category, slug=category_slug)
#          products = products.filter(category=category)
#
#      min_price = request.GET.get('min_price')
#      max_price = request.GET.get('max_price')
#
#      if min_price or max_price:
#          price_form = PriceFilterForm(request.GET)
#          if price_form.is_valid():
#              if min_price is not None:
#                  products = products.filter(price__gte=min_price)
#              if max_price is not None:
#                  products = products.filter(price__lte=max_price)
#              cart_product_forms = {}
#              quantities = {}
#              cart = Cart(request)
#              for product in products:
#                  quantity = cart.get_quantity(product)
#                  cart_product_forms[product.id] = CartAddProductForm(initial={
#                      "quantity": quantity,
#                      "product_id": product.id})
#                  quantities[product.id] = quantity
#              return render(request, 'shop/product/list_product.html',
#                            {'quantities': quantities, 'products': products})
#
#     chipest_product = products.order_by('price').first()
#     most_expensive_product =  products.order_by('-price').first()
#     price_form = PriceFilterForm(initial={
#         'min_price': chipest_product.price,
#         'max_price': most_expensive_product.price,
#     })
#
#     cart_product_forms = {}
#     quantities = {}
#     cart = Cart(request)
#     for product in products:
#         quantity = cart.get_quantity(product)
#         cart_product_forms[product.id] = CartAddProductForm(initial={
#             "quantity": quantity,
#             "product_id": product.id})
#         quantities[product.id] = quantity
#     return render(request, 'shop/product/list.html',
#                   {'category': category, 'categories': categories,
#                             'quantities': quantities, 'products': products,
#                             'price_form': price_form, 'cart_product_forms': cart_product_forms})

def product_list(request):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    category_slug = request.GET.get('category_slug')
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    price_form = PriceFilterForm(request.GET)
    if price_form.is_valid():
        min_price = price_form.cleaned_data.get('min_price')
        max_price = price_form.cleaned_data.get('max_price')
        if min_price is not None:
            products = products.filter(price__gte=min_price)
        if max_price is not None:
            products = products.filter(price__lte=max_price)

    cart = Cart(request)
    cart_product_forms = {
        product.id: CartAddProductForm(initial={
            "quantity": cart.get_quantity(product),
            "product_id": product.id
        }) for product in products
    }
    quantities = {
        product.id: cart.get_quantity(product)
        for product in products
    }

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'shop/product/list_product.html',
        { 'products': products, 'quantities': quantities,
                'cart_product_forms': cart_product_forms})

    return render(request, 'shop/product/list.html',
            {'category': category, 'categories': categories,
                    'quantities': quantities, 'products': products,
                    'price_form': price_form, 'cart_product_forms': cart_product_forms})


from .recommender import Recommender

def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart = Cart(request)
    quantity = cart.get_quantity(product)
    form = CartAddProductForm(initial={
        'quantity': quantity,
        "product_id": id})
    r = Recommender()
    recommended_products = r.suggested_products_for([product], 4)
    return render(request, 'shop/product/detail.html',
            {'product': product, 'cart_product_form': form,
                    'quantity': quantity, 'recommended_products': recommended_products})




