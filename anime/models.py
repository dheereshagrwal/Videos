from django.db import models

# Create your models here.


class Anime(models.Model):
    anime_name = models.CharField(max_length=255, blank=False, unique=True)
    anime_popularity = models.SmallIntegerField(blank=False, default=0)

    def __str__(self):
        return self.anime_name
