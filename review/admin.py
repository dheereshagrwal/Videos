from django.contrib import admin
from .models import ReviewRating,ReviewImage

# Register your models here.


class ReviewRatingAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'review_title', 'review_description',
                    'ip', 'status', 'created_date', 'updated_date',)
    list_editable = ('status',)
    list_filter = ('product', 'user', 'review_title', 'review_description',
                   'ip', 'status', 'created_date', 'updated_date')

class ReviewImageAdmin(admin.ModelAdmin):
    list_display = ('review_rating',)
    list_filter = ('review_rating',)
admin.site.register(ReviewRating, ReviewRatingAdmin)
admin.site.register(ReviewImage,ReviewImageAdmin)
