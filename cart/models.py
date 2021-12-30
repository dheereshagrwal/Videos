from django.db import models
from store.models import Product, Variation
from django.contrib.auth.models import User
# Create your models here.


class Cart(models.Model):
    cart_id = models.CharField(max_length=255, blank=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cart_id


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variations = models.ManyToManyField(Variation, blank=False)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    quantity = models.SmallIntegerField(default=0, blank=False)
    is_active = models.BooleanField(default=True)

    def subtotal(self):
        return self.quantity*self.product.price

    def __unicode__(self):
        return self.product
