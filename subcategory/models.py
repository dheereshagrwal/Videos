from django.db import models
from category.models import Category
from django.urls import reverse
# Create your models here.


class Subcategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory_name = models.CharField(
        max_length=255, blank=False, unique=True)
    slug = models.SlugField(max_length=255, blank=False, unique=True)
    subcategory_description = models.TextField(max_length=255, blank=False)
    subcategory_image = models.ImageField(
        upload_to='images/subcategories', blank=False)

    class Meta:
        verbose_name = 'subcategory'
        verbose_name_plural = 'subcategories'

    def __str__(self):
        return self.subcategory_name

    def category_name(self):
        return self.category.category_name
    def get_url(self):
        return reverse('products_by_category_or_subcategory', args=[self.slug])
