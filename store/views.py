from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404, HttpResponse
from . models import Product, ReviewRating
from category.models import Category
from subcategory.models import Subcategory
from cart.views import _get_cart_id
from cart.models import Cart, CartItem
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.contrib import messages
from .forms import ReviewForm
from order.models import OrderProduct


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
            in_cart = CartItem.objects.filter(
                user=request.user, product=single_product).exists()

        except Exception as e:
            raise e
        try:
            orderproduct = OrderProduct.objects.filter(
                user=request.user, product_id=single_product.id).exists()
        except OrderProduct.DoesNotExist:
            orderproduct = None
    else:
        orderproduct = None
        try:
            single_product = Product.objects.get(
                subcategory__slug=category_or_subcategory_slug, slug=product_slug)
            in_cart = CartItem.objects.filter(cart__cart_id=_get_cart_id(
                request), product=single_product).exists()

        except Exception as e:
            raise e

    # GEt the reviews
    reviews = ReviewRating.objects.filter(
        product_id=single_product.id, status=True)
    context = {'single_product': single_product, 'in_cart': in_cart,
               'orderproduct': orderproduct, 'reviews': reviews}
    return render(request, 'store/product-details.html', context)


def search(request):
    keywords = []
    products = []
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        keywords = keyword.split(' ')
        for key in keywords:
            for item in Product.objects.order_by('-created_date').filter(Q(product_description__icontains=key) | Q(product_name__icontains=key)):
                products.append(item)
        context = {'products': products, 'products_count': len(products)}
    return render(request, 'store/store.html', context)


def filter_by_anime(request):
    keywords = []
    products = []
    if 'anime_filter' in request.GET:
        keywords = request.GET.getlist('anime_filter')
        for key in keywords:
            for item in Product.objects.order_by('-created_date').filter(Q(product_description__icontains=key) | Q(product_name__icontains=key)):
                products.append(item)
    context = {'products': products, 'products_count': len(
        products), 'keywords': keywords}

    return render(request, 'store/store.html', context)


def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            # Updating the existing review
            review = ReviewRating.objects.get(
                user__id=request.user.id, product__id=product_id)
            form = ReviewForm(request.POST, request.FILES, instance=review)
            form.save()
            product = Product.objects.get(id=product_id)
            print(product)
            product.total_reviews += 1
            product.total_ratings_sum+=review.rating
            product.average_rating = product.total_ratings_sum/product.total_reviews
            product.save()
            messages.success(request, 'Thank you for your form update!')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST, request.FILES)
            if form.is_valid():
                data = ReviewRating()
                data.review_title = form.cleaned_data['review_title']
                data.review_description = form.cleaned_data['review_description']
                data.rating = form.cleaned_data['rating']
                data.review_images = form.cleaned_data['review_images']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                product = Product.objects.get(id=product_id)
                product.total_reviews += 1
                product.total_ratings_sum += review.rating
                product.average_rating = product.total_ratings_sum/product.total_reviews
                product.save()
                messages.success(
                    request, 'Thank you for your form submission!')
                return redirect(url)
            pass
    return redirect('home')
