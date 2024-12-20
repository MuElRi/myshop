from django.contrib import admin
from .models import *
from attachment.models import Attachment
from django.contrib.contenttypes.admin import GenericStackedInline

class AttachmentInLine(GenericStackedInline):
    model = Attachment
    extra = 1  # Количество пустых форм для добавления новых вложений

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'rating', 'text', 'created', 'updated', 'active')
    list_filter = ('active', 'created', 'updated')
    list_editable = ('active',)
    inlines = [AttachmentInLine]

