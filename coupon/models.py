from django.db import models

# Create your models here.


class Coupon(models.Model):
    coupon_name = models.CharField(max_length=255, blank=False, unique=True)
    coupon_value = models.DecimalField(
        max_digits=3, decimal_places=2, default=0.00)
    def __str__(self):
        return self.coupon_name