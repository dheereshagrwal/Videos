from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile
from django.utils.html import format_html
# class UserProfileAdmin(admin.ModelAdmin):
#     def user_avatar(self,object):
#         return format_html('<img src="{}" width="30" style="border-radius:50%;">'.format(object.profile_picture.url))
#     user_avatar.short_description = 'Profile picture'
#     list_display = ('user','city','state','country','pin')

# admin.site.register(UserProfile, UserProfileAdmin)