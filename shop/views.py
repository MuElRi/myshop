from celery.worker.control import active
from django.db.models import Avg
from django.db.models.expressions import result
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from netaddr.ip.iana import query

from .models import Category, Product
from cart.forms import CartAddProductForm
from cart.cart import Cart
from .forms import PriceFilterForm
from .recommender import Recommender
from comments.forms import *
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.db.models import F
from django.contrib.postgres.search import TrigramSimilarity


class ProductDetailView(DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'shop/product/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = context['product']
        cart = Cart(self.request)
        context['cart_product_form'] = CartAddProductForm(initial={
                                        'quantity': cart.get_quantity(product),
                                        'product_id': product.id})
        context['quantity'] = cart.get_quantity(product)
        # Добавляем рекомендуемые товары
        # r = Recommender()
        # recommended_products = r.suggested_products_for([product], 5)
        # context['recommended_products'] = recommended_products

        comments = product.comments.filter(active=True)
        context['comments'] = comments
        context['average_rating'] = comments.aggregate(average=Avg('rating'))['average']

        if self.request.user.is_authenticated:
            context['comment_form'] = CommentForm()
            attachment_form = AttachmentFormSet()
            attachment_form.queryset = Attachment.objects.none()
            context['attachment_form'] = attachment_form
        return context


class ProductListView(ListView):
    model = Product
    template_name = 'shop/product/list.html'
    context_object_name = 'products'

    def get_queryset(self):
        # Базовый запрос для получения доступных товаров
        queryset = Product.published.all()

        #поиск по полям
        q = self.request.GET.get('q')
        if q:
            # queryset = queryset.annotate(
            #     name_similarity=TrigramSimilarity('name', q),
            #     description_similarity=TrigramSimilarity('description', q),
            #     similarity=F('name_similarity') + F('description_similarity')
            # ).filter(
            #     similarity__gt=0.1  # Фильтруем по минимальной похожести
            # ).order_by('-similarity')  # Сортируем по убыванию похожести
            search_vector = SearchVector('name', weight='A') + \
                            SearchVector('description', weight='B')
            search_query = SearchQuery(q)
            queryset = queryset.annotate(
                search=search_vector,
                rank=SearchRank(search_vector, search_query)
            ).filter(rank__gte=0.2).order_by('-rank')

        # Фильтрация по категории
        category_slug = self.request.GET.get('category_slug')
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            queryset = queryset.filter(category=category)
            self.category = category
        else:
            self.category = None

        # Фильтрация по цене
        self.price_form = PriceFilterForm(self.request.GET)
        if self.price_form.is_valid():
            min_price = self.price_form.cleaned_data.get('min_price')
            max_price = self.price_form.cleaned_data.get('max_price')
            if min_price is not None:
                queryset = queryset.filter(price__gte=min_price)
            if max_price is not None:
                queryset = queryset.filter(price__lte=max_price)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = Cart(self.request)
        products = context['products']

        # Добавляем данные о категории, формах для корзины
        context['category'] = self.category
        context['categories'] = Category.objects.all()
        context['price_form'] = self.price_form
        context['cart_product_forms'] = {
            product.id: CartAddProductForm(initial={
                'quantity': cart.get_quantity(product),
                'product_id': product.id
            }) for product in products
        }
        context['quantities'] = {
            product.id: cart.get_quantity(product)
            for product in products
        }

        return context

    def render_to_response(self, context, **response_kwargs):
        # Проверяем, является ли запрос AJAX
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return render(self.request, 'shop/product/list_product.html',
                          context, **response_kwargs)
        return super().render_to_response(context, **response_kwargs)



# def product_list(request):
#     category = None
#     categories = Category.objects.all()
#     products = Product.objects.filter(available=True)
#
#     category_slug = request.GET.get('category_slug')
#     if category_slug:
#         category = get_object_or_404(Category, slug=category_slug)
#         products = products.filter(category=category)
#
#     price_form = PriceFilterForm(request.GET)
#     if price_form.is_valid():
#         min_price = price_form.cleaned_data.get('min_price')
#         max_price = price_form.cleaned_data.get('max_price')
#         if min_price is not None:
#             products = products.filter(price__gte=min_price)
#         if max_price is not None:
#             products = products.filter(price__lte=max_price)
#
#     cart = Cart(request)
#     cart_product_forms = {
#         product.id: CartAddProductForm(initial={
#             "quantity": cart.get_quantity(product),
#             "product_id": product.id
#         }) for product in products
#     }
#     quantities = {
#         product.id: cart.get_quantity(product)
#         for product in products
#     }
#
#     if request.headers.get('x-requested-with') == 'XMLHttpRequest':
#         return render(request, 'shop/product/list_product.html',
#         { 'products': products, 'quantities': quantities,
#                 'cart_product_forms': cart_product_forms})
#
#     return render(request, 'shop/product/list.html',
#             {'category': category, 'categories': categories,
#                     'quantities': quantities, 'products': products,
#                     'price_form': price_form, 'cart_product_forms': cart_product_forms})


# def product_detail(request, id, slug):
#     product = get_object_or_404(Product, id=id, slug=slug, available=True)
#     cart = Cart(request)
#     quantity = cart.get_quantity(product)
#     form = CartAddProductForm(initial={
#         'quantity': quantity,
#         "product_id": id})
#     r = Recommender()
#     recommended_products = r.suggested_products_for([product], 4)
#     return render(request, 'shop/product/detail.html',
#             {'product': product, 'cart_product_form': form,
#                     'quantity': quantity, 'recommended_products': recommended_products})



