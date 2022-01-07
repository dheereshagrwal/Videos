from django.contrib import admin
from .models import Anime
# Register your models here.

class AnimeAdmin(admin.ModelAdmin):
    list_display = ('anime_name', 'anime_popularity',)
    list_filter = ('anime_name', 'anime_popularity',)
    list_editable = ('anime_popularity',)


admin.site.register(Anime, AnimeAdmin)
