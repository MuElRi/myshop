from django.conf import settings
from django.db import models
from django.db.models import ForeignKey
from django.urls import reverse
from django.contrib.contenttypes.fields import GenericRelation
from attachment.models import Attachment

class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ['name']
        indexes = [models.Index(fields=['name'])]
        verbose_name = 'category'
        verbose_name_plural = 'categories'


    def __str__(self):
        return self.name

    def get_absolute_url(self):
        # Генерация URL для категории с параметром ?category=<id>
        return f"{reverse('shop:product_list')}?category_slug={self.slug}"



class AvailableManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(available=True)

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    description = models.TextField(blank=True)
    price = models.IntegerField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    published = AvailableManager()
    objects = models.Manager()
    attachments = GenericRelation(Attachment)

    class Meta:
        ordering = ['name']
        indexes = [models.Index(fields=['id', 'slug']),
                   models.Index(fields=['name']),
                   models.Index(fields=['-created'])]

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])

    def __str__(self):
        return self.name




