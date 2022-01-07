from django.contrib import admin
from .models import Coupon
# Register your models here.


class CouponAdmin(admin.ModelAdmin):
    list_display = ('coupon_name', 'coupon_value',)
    list_filter = ('coupon_name', 'coupon_value',)
    list_editable = ('coupon_value',)


admin.site.register(Coupon, CouponAdmin)
