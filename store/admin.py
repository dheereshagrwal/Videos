from django.contrib import admin
from .models import Product, Variation, ReviewRating, ProductImages,AnimeName
# Register your models here.
import admin_thumbnails


@admin_thumbnails.thumbnail('images')
class ProductImagesInline(admin.TabularInline):
    model = ProductImages
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'stock', 'category','subcategory', 'anime_name', 'popularity', 'created_date', 'modified_date', 'is_available', 'is_on_sale', 'ordered_quantity', 'average_rating', 'total_reviews', 'total_ratings_sum')
    prepopulated_fields = {'slug': ('product_name',), }
    list_editable = ('is_available','is_on_sale',)
    list_filter = ('product_name', 'price', 'stock', 'category',
                   'subcategory', 'anime_name', 'popularity','created_date', 'modified_date', 'is_available', 'is_on_sale', 'ordered_quantity', 'average_rating', 'total_reviews', 'total_ratings_sum')
    inlines = [ProductImagesInline]


class VariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'variation_category',
                    'variation_value', 'is_active')
    list_editable = ('is_active',)
    list_filter = ('product', 'variation_category',
                   'variation_value', 'is_active')


class ReviewRatingAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'review_title', 'review_description',
                    'review_image', 'ip', 'status', 'created_date', 'updated_date',)
    list_editable = ('status',)
    list_filter = ('product', 'user', 'review_title', 'review_description', 'review_image',
                   'ip', 'status', 'created_date', 'updated_date')


class AnimeNameAdmin(admin.ModelAdmin):
    list_display = ('anime_name', 'anime_popularity',)
    list_filter = ('anime_name', 'anime_popularity',)
    list_editable = ('anime_popularity',)

admin.site.register(Product, ProductAdmin)
admin.site.register(Variation, VariationAdmin)
admin.site.register(ReviewRating, ReviewRatingAdmin)
admin.site.register(ProductImages)
admin.site.register(AnimeName,AnimeNameAdmin)
