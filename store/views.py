from django.shortcuts import render, get_object_or_404
from django.http import Http404
from . models import Product
from category.models import Category
from subcategory.models import Subcategory

# Create your views here.


def store(request, category_or_subcategory_slug=None):
    category = None
    products = None
    subcategory = None
    if category_or_subcategory_slug is not None:
        try:
            category = Category.objects.get(slug=category_or_subcategory_slug)
            products = Product.objects.filter(
                category=category, is_available=True)
        except:
            try:
                subcategory = Subcategory.objects.get(slug=category_or_subcategory_slug)
                products = Product.objects.filter(
                    subcategory=subcategory, is_available=True)
            except:
                raise Http404("Given query not found....")
        
        products_count = products.count()

    else:
        products = Product.objects.all().filter(is_available=True)
        products_count = products.count()

    context = {'products': products, 'products_count': products_count}
    return render(request, 'store/store.html', context)

def product_details(request,category_or_subcategory_slug,product_slug):
    try:
        single_product = Product.objects.get(subcategory__slug=category_or_subcategory_slug,slug=product_slug)
    except Exception as e:
        raise e
    context = {'single_product': single_product,}
    return render(request, 'store/product-details.html',context)