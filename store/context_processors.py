from .models import Product


def popular_products(request):
    popular_products = Product.objects.filter(
        popularity__gte=1).order_by('-popularity')
    return dict(popular_products=popular_products)


def newest_arrivals(request):
    from datetime import datetime
    from django.utils.timezone import get_current_timezone
    # year 2022, date 5, month 1, time 2.00pm hence 14, 2 means 2 minutes, 3 means 3 seconds 
    date_ = datetime(2022, 1, 5, 14, 2, 3,   tzinfo=get_current_timezone())
    newest_arrivals = Product.objects.filter(
        created_date__gte=date_).order_by('-created_date')

    return dict(newest_arrivals=newest_arrivals)

