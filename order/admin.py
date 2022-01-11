from django.contrib import admin
from .models import Order, OrderProduct
# Register your models here.


class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    readonly_fields = ('user', 'product',
                       'quantity', 'product_price', 'ordered')
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'full_name', 'phone', 'email',
                    'city', 'order_total', 'tax', 'delivery_charge', 'discount', 'status', 'is_ordered', 'created_at', 'gift_charge', ]
    list_filter = ['status', 'is_ordered']
    search_fields = ['order_number',
                     'first_name', 'last_name', 'phone', 'email']
    list_per_page = 20
    inlines = [OrderProductInline]


class OrderProductAdmin(admin.ModelAdmin):
    list_display = ('user', 'product',
                    'quantity', 'product_price', 'ordered')
    list_filter = ('user', 'product',
                   'quantity', 'product_price', 'ordered')


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct, OrderProductAdmin)

