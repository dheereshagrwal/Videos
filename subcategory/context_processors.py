from .models import Subcategory


def subcategory_links(request):
    subcategory_links = Subcategory.objects.all()
    return dict(subcategory_links=subcategory_links)
