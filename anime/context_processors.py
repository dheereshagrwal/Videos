from .models import Anime

def animes(request):
    animes = Anime.objects.all()
    return dict(animes=animes)
