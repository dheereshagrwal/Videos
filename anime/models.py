from django.db import models
class Anime(models.Model):
    anime_name = models.CharField(max_length=255, blank=False, unique=True)
    slug = models.SlugField(max_length=255, blank=False, unique=True,null=True)
    anime_popularity = models.SmallIntegerField(blank=False, default=0)
    anime_description = models.CharField(max_length=255, blank=False,null=True)

    def __str__(self):
        return self.anime_name
