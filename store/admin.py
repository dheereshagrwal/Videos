from django.contrib import admin
from .models import Product, Variation, ReviewRating, ProductImages
# Register your models here.
import admin_thumbnails


@admin_thumbnails.thumbnail('images')
class ProductImagesInline(admin.TabularInline):
    model = ProductImages
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'stock', 'category',
                    'subcategory', 'modified_date', 'is_available', 'is_on_sale', 'ordered_quantity', 'average_rating', 'total_reviews', 'total_ratings_sum')
    prepopulated_fields = {
        'product_description': ('product_name',), 'slug': ('product_name',), }
    list_filter = ('product_name', 'price', 'stock', 'category',
                   'subcategory', 'modified_date', 'is_available', 'is_on_sale', 'ordered_quantity', 'average_rating', 'total_reviews', 'total_ratings_sum')
    inlines = [ProductImagesInline]


class VariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'variation_category',
                    'variation_value', 'is_active')
    list_editable = ('is_active',)
    list_filter = ('product', 'variation_category',
                   'variation_value', 'is_active')


class ReviewRatingAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'review_title', 'review_description',
                    'review_images', 'ip', 'status', 'created_date', 'updated_date',)
    list_editable = ('status',)
    list_filter = ('product', 'user', 'review_title', 'review_description', 'review_images',
                   'ip', 'status', 'created_date', 'updated_date')


admin.site.register(Product, ProductAdmin)
admin.site.register(Variation, VariationAdmin)
admin.site.register(ReviewRating, ReviewRatingAdmin)
admin.site.register(ProductImages)
