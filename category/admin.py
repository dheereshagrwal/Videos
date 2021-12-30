from django.contrib import admin
from .models import Category
# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ('category_name',), 'category_description': ('category_name',), }
    list_display = ('category_name', 'slug', 'category_description',)
    list_filter = ('category_name', 'slug', 'category_description',)


admin.site.register(Category, CategoryAdmin)
