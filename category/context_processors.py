from .models import Category

def category_links(request):
    category_links = Category.objects.all()
    return dict(category_links=category_links)
