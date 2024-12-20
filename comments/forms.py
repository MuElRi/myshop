from django import forms
from .models import Comment
from attachment.models import Attachment
from django.forms import modelformset_factory, modelform_factory, Select, Textarea

CommentForm = modelform_factory(
    Comment,
    fields=['rating', 'text'],
    widgets={
        'rating': Select(choices=[(i, str(i)) for i in range(1, 6)]),
        'text': Textarea(attrs={'placeholder': 'Write your comment'}),
    }
)

AttachmentForm = modelform_factory(Attachment, fields = ['file'])

AttachmentFormSet = modelformset_factory(
    Attachment,
    fields = ['file'],
    extra=3,  # Число пустых форм для новых вложений
    can_delete=True,  # Возможность удаления старых вложений
)


