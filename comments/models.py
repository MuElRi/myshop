from django.conf import settings
from django.db import models
from shop.models import Product
from django.contrib.contenttypes.fields import GenericRelation
from attachment.models import Attachment


class ActivatedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(active=True)

class Comment(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="comments",
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='comments',
        on_delete=models.CASCADE,
    )
    rating = models.IntegerField(choices=[
        (i, str(i)) for i in range(1, 6)],
        default=5,
    )
    text = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    attachments = GenericRelation(Attachment)

    actived = ActivatedManager()
    objects = models.Manager()


    class Meta:
        ordering = ['-created']
        indexes = [models.Index(fields=['-created'])]
        constraints  = [
            models.UniqueConstraint(fields=['user', 'product'],
            name='unique_user_product_comment'),
        ]

    def __str__(self):
        return f'Comment by {self.user.username} on {self.product.name}]'


