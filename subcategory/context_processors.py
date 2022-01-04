from .models import Subcategory


def subcategory_links(request):
    subcategory_links = Subcategory.objects.all()
    for subcategory in subcategory_links:
        print(subcategory.get_url)
    return dict(subcategory_links=subcategory_links)
