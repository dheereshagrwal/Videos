from django.contrib import admin
from .models import Address


class AddressAdmin(admin.ModelAdmin):
    list_display = ['phone', 'email','state','city', 'pin',]
    list_filter = ['phone', 'email', 'state', 'city', 'pin', ]
    search_fields = ['phone', 'email', 'state', 'city', 'pin', ]
    list_per_page = 20

admin.site.register(Address, AddressAdmin)

