from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponse
from . models import Product
from category.models import Category
from subcategory.models import Subcategory
from cart.views import _get_cart_id
from cart.models import Cart, CartItem
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
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
            paginator = Paginator(products, 3)
            page = request.GET.get('page')
            paged_products = paginator.get_page(page)
        except:
            try:
                subcategory = Subcategory.objects.get(
                    slug=category_or_subcategory_slug)
                products = Product.objects.filter(
                    subcategory=subcategory, is_available=True)
                paginator = Paginator(products, 3)
                page = request.GET.get('page')
                paged_products = paginator.get_page(page)
            except:
                raise Http404("Given query not found....")

        products_count = products.count()

    else:
        products = Product.objects.all().filter(is_available=True).order_by('id')
        paginator = Paginator(products, 3)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        products_count = products.count()

    context = {'products': paged_products, 'products_count': products_count}
    return render(request, 'store/store.html', context)


def product_details(request, category_or_subcategory_slug, product_slug):
    # cart_items = CartItem.objects.all().filter(user=request.user).exists()
    
    if request.user.is_authenticated:
        try:
            single_product = Product.objects.get(
                subcategory__slug=category_or_subcategory_slug, slug=product_slug)
            in_cart = CartItem.objects.filter(user=request.user, product=single_product).exists()

        except Exception as e:
            raise e
    else:
            
        try:
            single_product = Product.objects.get(
                subcategory__slug=category_or_subcategory_slug, slug=product_slug)
            in_cart = CartItem.objects.filter(cart__cart_id=_get_cart_id(
                request), product=single_product).exists()

        except Exception as e:
            raise e
    context = {'single_product': single_product, 'in_cart': in_cart}
    return render(request, 'store/product-details.html', context)


def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(
                Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            products_count = products.count()
        context = {'products': products,'products_count':products_count}
    return render(request, 'store/store.html', context)
