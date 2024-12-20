from itertools import product

from django.db.models import Avg
from django.http import HttpResponse
from django.views.generic import *
from attachment.models import Attachment
from shop.models import Product
from .forms import CommentForm, AttachmentFormSet
from .models import Comment
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string


class CommentCreateView(FormView):
    http_method_names = ['post']
    comment_form_class = CommentForm
    attachment_formset_class = AttachmentFormSet
    template_name = 'shop/product/comment.html'

    def get_forms(self):
        comment_form =  self.comment_form_class(data=self.request.POST)
        attachment_formset = self.attachment_formset_class(
            data=self.request.POST,
            files=self.request.FILES,
            queryset=Attachment.objects.none()
        )
        return comment_form, attachment_formset

    def post(self, request, *args, **kwargs):
        #Пользователь может оставлять только один комментарий под товаром
        if Comment.objects.filter(user = self.request.user,
                product__id = self.kwargs['product_id']).exists():
            return JsonResponse({'success': False})

        comment_form, attachment_formset = self.get_forms()

        if comment_form.is_valid() and attachment_formset.is_valid():
            return self.form_valid(
                comment_form=comment_form,
                attachment_formset=attachment_formset
            )
        else:
            return self.form_invalid(
                comment_form=comment_form,
                attachment_formset=attachment_formset
            )

    def form_valid(self, comment_form, attachment_formset):
        comment = comment_form.save(commit=False)
        product = get_object_or_404(Product, id=self.kwargs['product_id'])
        comment.product = product
        comment.user = self.request.user
        comment.save()

        for attachment_form in attachment_formset:
            if attachment_form.cleaned_data.get('file'):
                attachment = attachment_form.save(commit=False)
                attachment.content_object = comment  # Привязываем через ContentType
                attachment.save()
        attachment = comment.attachments
        context = {
            'request': self.request,
            'comment': comment,
            'attachment': attachment
        }
        comment_html = render_to_string(self.template_name, context)
        average_rating = Comment.actived.filter(product = self.kwargs['product_id']
                                     ).aggregate(average=Avg('rating'))['average']

        return JsonResponse({
            'success': True,
            'comment_html': comment_html,
            'average_rating': average_rating,
        })

    def form_invalid(self, **kwargs):
        return JsonResponse({'success': False})




class CommentDeleteView(View):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, id=self.kwargs['comment_id'], user=request.user)
        comment.delete()
        # average_rating = Comment.actived.filter(product=self.kwargs['product_id']
        #                                         ).aggregate(average=Avg('rating'))['average']
        average_rating = Comment.actived.filter(product=self.kwargs['product_id']
                                                ).aggregate(average=Avg('rating'))['average']
        return JsonResponse({
            'success': True,
            'average_rating': average_rating,
        })

