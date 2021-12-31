from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from subcategory.models import Subcategory
from category.models import Category
from django.urls import reverse
# Create your models here.
from django.db.models import Avg, Count


class Product(models.Model):
    product_name = models.CharField(max_length=255, unique=True, blank=False)
    slug = models.SlugField(max_length=255, unique=True, blank=False)
    product_description = models.CharField(
        max_length=255, blank=False)
    price = models.SmallIntegerField(
        default=0, validators=[MaxValueValidator(32767), MinValueValidator(1)])
    popularity_score = models.SmallIntegerField(
        default=1, validators=[MaxValueValidator(32767), MinValueValidator(1)], blank=False)
    images = models.ImageField(upload_to='images/products',blank=False)
    stock = models.SmallIntegerField(default=10, blank=False)
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    is_on_sale = models.BooleanField(default=True)
    ordered_quantity = models.IntegerField(default=0, blank=False)
    average_rating = models.FloatField(default=0,blank=False)
    total_reviews = models.IntegerField(default=0,blank=False)
    total_ratings_sum= models.IntegerField(default=0, blank=False)

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

    def gifts(self):
        return super(VariationManager, self).filter(variation_category='gift', is_active=True)


variation_category_choice = (
    ('material', 'material'),
    ('color', 'color'),
    ('size', 'size'),
    ('gift', 'gift'),
)


class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(
        max_length=255, choices=variation_category_choice)
    variation_value = models.CharField(max_length=255, default='Default',blank=False)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now=True)
    variation_price =models.SmallIntegerField(default=0)
    objects = VariationManager()

    def __str__(self):
        return self.variation_value


class ReviewRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review_title = models.CharField(max_length=255, blank=True)
    review_description = models.TextField(max_length=255, blank=True)
    rating = models.SmallIntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)],blank = False,default=1)
    review_images = models.ImageField(
        upload_to='images/reviews', blank=True)
    ip = models.CharField(max_length=255, blank=False)
    status = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.review_title


class ProductImages(models.Model):
    product=models.ForeignKey(Product,default=None,on_delete=models.CASCADE)
    images=models.ImageField(upload_to='images/products')
    def __str__(self):
        return self.product.product_name
    class Meta:
        verbose_name = "productimages"
        verbose_name_plural = "product images"

        
        
