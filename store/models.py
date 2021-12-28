from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from subcategory.models import Subcategory
from category.models import Category
from django.urls import reverse
# Create your models here.


class Product(models.Model):
    product_name = models.CharField(max_length=255, unique=True, blank=False)
    slug = models.SlugField(max_length=255, unique=True, blank=False)
    description = models.TextField(max_length=255, blank=False)
    price = models.SmallIntegerField(
        default=0, validators=[MaxValueValidator(32767), MinValueValidator(1)])
    popularity_score = models.SmallIntegerField(
        default=1, validators=[MaxValueValidator(32767), MinValueValidator(1)], blank=False)
    images = models.ImageField(upload_to='images/products')
    stock = models.SmallIntegerField(default=10, blank=False)
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    is_on_sale = models.BooleanField(default=True)

    def get_url(self):
        return reverse('product_details', args=[self.subcategory.slug, self.slug])

    def __str__(self):
        return self.product_name


class VariationManager(models.Manager):
    def materials(self):
        return super(VariationManager, self).filter(variation_category='material', is_active=True)

    def colors(self):
        return super(VariationManager, self).filter(variation_category='color', is_active=True)

    def sizes(self):
        return super(VariationManager, self).filter(variation_category='size', is_active=True)


variation_category_choice = (
    ('material', 'material'),
    ('color', 'color'),
    ('size', 'size'),
)


class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(
        max_length=255, choices=variation_category_choice)
    variation_value = models.CharField(max_length=255, default='Default')
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now=True)
    objects = VariationManager()

    def __str__(self):
        return self.variation_value
