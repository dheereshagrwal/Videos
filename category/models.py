from django.db import models
from django.urls import reverse

# Create your models here.


class Category(models.Model):
    category_name = models.CharField(max_length=255, blank=False, unique=True)
    slug = models.SlugField(max_length=255, blank=False, unique=True)
    category_description = models.CharField(max_length=255, blank=False)
    category_image = models.ImageField(
        upload_to='images/categories', blank=False)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.category_name

    def get_url(self):
        return reverse('products_by_view', args=[self.slug])
