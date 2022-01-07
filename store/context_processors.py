from .models import Product

def popular_products(request):
    popular_products = Product.objects.filter(popularity__gte=1).order_by('-popularity')
    return dict(popular_products=popular_products)

def newest_arrivals(request):
    from datetime import date
    date_ = date(2022, 1, 5)
    newest_arrivals = Product.objects.filter(created_date__gte=date_).order_by('-created_date')
    return dict(newest_arrivals=newest_arrivals)
