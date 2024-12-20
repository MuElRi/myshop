from django.contrib import admin

from shop.models import Product, Category
from attachment.models import Attachment
from django.contrib.contenttypes.admin import GenericStackedInline


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

class AttachmentInLine(GenericStackedInline):
    model = Attachment
    extra = 1  # Количество пустых форм для добавления новых вложений

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'price', 'available', 'created', 'updated')
    list_filter = ('available', 'created', 'updated')
    list_editable = ('price', 'available')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [AttachmentInLine]