from django.contrib import admin
from .models import Product, Variation, ProductImages
import admin_thumbnails


@admin_thumbnails.thumbnail('images')
class ProductImagesInline(admin.TabularInline):
    model = ProductImages
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'stock', 'category','subcategory', 'anime', 'popularity', 'created_date', 'modified_date', 'is_available', 'is_on_sale', 'ordered_quantity', 'average_rating', 'total_reviews', 'total_ratings_sum')
    prepopulated_fields = {'slug': ('product_name',), }
    list_editable = ('is_available','is_on_sale',)
    list_filter = ('product_name', 'price', 'stock', 'category',
                   'subcategory', 'anime', 'popularity','created_date', 'modified_date', 'is_available', 'is_on_sale', 'ordered_quantity', 'average_rating', 'total_reviews', 'total_ratings_sum')
    inlines = [ProductImagesInline]


class VariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'variation_category',
                    'variation_value', 'is_active')
    list_editable = ('is_active',)
    list_filter = ('product', 'variation_category',
                   'variation_value', 'is_active')







admin.site.register(Product, ProductAdmin)
admin.site.register(Variation, VariationAdmin)
admin.site.register(ProductImages)

