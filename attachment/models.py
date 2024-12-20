import os
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation


class Attachment(models.Model):
    TYPE_CHOICES = [
        ('image', 'Image'),
        ('video', 'Video'),
    ]

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    file = models.FileField(upload_to='attachments/%Y/%m/%d')
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']

    def save(self, *args,  **kwargs):
        # Определение типа файла на основе расширения
        file_extension = os.path.splitext(self.file.name)[1].lower()

        # Проверка на допустимые типы файлов
        if file_extension in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff']:
            self.type = 'image'
        elif file_extension in ['.mp4', '.avi', '.mov', '.mkv', '.flv']:
            self.type = 'video'
        else:
            raise ValidationError(
                f"Unsupported file type: {file_extension}. Only image and video files are allowed.")

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.get_type_display()} for {self.content_object}"

