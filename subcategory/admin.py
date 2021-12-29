from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Subcategory
# Register your models here.


class SubcategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('subcategory_name',)}
    list_display = ('subcategory_name', 'slug',
                    'category_name', 'subcategory_description',)
    list_filter = ('subcategory_name', 'slug',
                    'category', 'subcategory_description',)


admin.site.register(Subcategory, SubcategoryAdmin)
