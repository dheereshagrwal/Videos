from django.contrib import admin
from .models import ReviewRating

# Register your models here.


class ReviewRatingAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'review_title', 'review_description',
                    'review_image', 'ip', 'status', 'created_date', 'updated_date',)
    list_editable = ('status',)
    list_filter = ('product', 'user', 'review_title', 'review_description', 'review_image',
                   'ip', 'status', 'created_date', 'updated_date')
admin.site.register(ReviewRating, ReviewRatingAdmin)
