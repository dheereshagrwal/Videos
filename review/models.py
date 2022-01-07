from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from store.models import Product
# Create your models here.


class ReviewRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review_title = models.CharField(max_length=255, blank=True)
    review_description = models.TextField(max_length=255, blank=True)
    rating = models.SmallIntegerField(validators=[MaxValueValidator(
        5), MinValueValidator(1)], blank=False, default=1)
    # review_image = models.ImageField(upload_to='images/reviews', blank=True)
    ip = models.CharField(max_length=255, blank=False)
    status = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.review_title


class Images(models.Model):
    review_rating = models.ForeignKey(ReviewRating, on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to='images/reviews', null=True, blank=True)
