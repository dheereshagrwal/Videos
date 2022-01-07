from django.contrib import admin
from .models import Anime

class AnimeAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('anime_name',)}
    list_display = ('anime_name', 'anime_popularity',)
    list_filter = ('anime_name', 'anime_popularity',)
    list_editable = ('anime_popularity',)


admin.site.register(Anime, AnimeAdmin)
