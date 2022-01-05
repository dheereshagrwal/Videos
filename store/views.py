from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404, HttpResponse
from . models import Product, ReviewRating, ProductImages
from category.models import Category
from subcategory.models import Subcategory
from cart.views import _get_cart_id
from cart.models import Cart, CartItem
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.contrib import messages
from .forms import ReviewForm
from order.models import OrderProduct


# def store(request, category_slug=None, subcategory_slug=None):
#     # print(request.META.get('HTTP_REFERER'))

#     category = None
#     products = None
#     subcategory = None
#     if category_slug:
#         try:
#             category = Category.objects.get(slug=category_slug)
#             if subcategory_slug:
#                 subcategory = Subcategory.objects.get(
#                     category=category, slug=subcategory_slug)
#                 products = Product.objects.filter(
#                     category=category, subcategory=subcategory, is_available=True).order_by('id')
#             else:
#                 products = Product.objects.filter(
#                     category=category, is_available=True).order_by('id')
#             paginator = Paginator(products, 3)
#             page = request.GET.get('page')
#             paged_products = paginator.get_page(page)
#             products_count = products.count()
#             context = {'products': paged_products,
#                        'products_count': products_count}
#         except:
#             raise Http404("Given query not found....")
#     # Getting all the products
#     else:
#         sort_by = 'id'
#         for sort_category in request.GET.getlist('sort_by'):
#             # '-' is added because we want in decreasing order
#             if sort_category == "price":
#                 sort_by = 'price'
#             else:
#                 sort_by = '-' + sort_category
#         # request.session['sort_by'] = sort_by
#         # request.session.modified = True
#         products = Product.objects.all().filter(is_available=True)
#         products = products.order_by(sort_by)
#         paginator = Paginator(products, 3)
#         page = request.GET.get('page')
#         paged_products = paginator.get_page(page)
#         products_count = products.count()
#         context = {'products': paged_products,
#                    'products_count': products_count, 'sort_by': sort_by}

#     return render(request, 'store/store.html', context)


def store(request, category_slug=None, subcategory_slug=None):
    # print(request.META.get('HTTP_REFERER'))

    category = None
    products = None
    subcategory = None
    if category_slug:
        try:
            category = Category.objects.get(slug=category_slug)
            # If there is a subcategory
            if subcategory_slug:
                subcategory = Subcategory.objects.get(
                    category=category, slug=subcategory_slug)
                products = Product.objects.filter(
                    category=category, subcategory=subcategory, is_available=True).order_by('id')
            # If there is only category
            else:
                products = Product.objects.filter(
                    category=category, is_available=True).order_by('id')
            paginator = Paginator(products, 3)
            page = request.GET.get('page')
            paged_products = paginator.get_page(page)
            products_count = products.count()
            context = {'products': paged_products,
                       'products_count': products_count}
        except:
            raise Http404("Given query not found....")

    else:
        sort_by = 'id'
        for sort_category in request.GET.getlist('sort_by'):
            # '-' is added because we want in decreasing order
            if sort_category == "price":
                sort_by = 'price'
            else:
                sort_by = '-' + sort_category
        is_categories = False
        is_subcategories = False
        categories = request.GET.getlist('category_filter')
        subcategories = request.GET.getlist('subcategory_filter')
        if categories:
            is_categories = True
        if subcategories:
            is_subcategories = True
        if is_categories and (not is_subcategories):
            # This is products list not to be confused with products
            products = []
            for category in categories:
                for item in Product.objects.order_by(sort_by).filter(category__category_name=category):
                    products.append(item)
            products_count = len(products)
        if is_subcategories:
            products = []
            filter_dict = {}
            for filter_subcat in subcategories:
                filter_cat = Subcategory.objects.get(
                    subcategory_name=filter_subcat).category_name()
                if filter_cat in filter_dict:
                    filter_dict[filter_cat].append(filter_subcat)
                else:
                    filter_dict[filter_cat] = [filter_subcat]

            for cat_ in categories:
                if cat_ not in filter_dict:
                    for item in Product.objects.filter(category__category_name=cat_):
                        products.append(item)
                else:
                    for subcat_ in filter_dict[cat_]:
                        for item in Product.objects.filter(category__category_name=cat_, subcategory__subcategory_name=subcat_):
                            products.append(item)

            products_count = len(products)
        # Getting all the products
        if (not is_categories) and (not is_subcategories):
            products = Product.objects.all().filter(is_available=True)
            products = products.order_by(sort_by)
            products_count = products.count()
        paginator = Paginator(products, 10)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        context = {'products': paged_products,
                   'products_count': products_count, 'sort_by': sort_by}

    return render(request, 'store/store.html', context)


def product_details(request, category_slug, subcategory_slug, product_slug):
    # cart_items = CartItem.objects.all().filter(user=request.user).exists()

    if request.user.is_authenticated:
        try:
            single_product = Product.objects.get(
                subcategory__slug=subcategory_slug, slug=product_slug)
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
                subcategory__slug=subcategory_slug, slug=product_slug)
            in_cart = CartItem.objects.filter(cart__cart_id=_get_cart_id(
                request), product=single_product).exists()

        except Exception as e:
            raise e

    # GEt the reviews
    reviews = ReviewRating.objects.filter(
        product_id=single_product.id, status=True)
    # Get the product images
    product_images = ProductImages.objects.filter(product_id=single_product.id)
    context = {'single_product': single_product, 'in_cart': in_cart,
               'orderproduct': orderproduct, 'reviews': reviews, 'product_images': product_images}
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
    # print(request.META.get('HTTP_REFERER'))
    anime_list = []
    products = []
    if 'anime_filter' in request.GET:
        anime_list = request.GET.getlist('anime_filter')
        for anime in anime_list:
            for item in Product.objects.order_by('-created_date').filter(Q(product_description__icontains=anime) | Q(product_name__icontains=anime)):
                products.append(item)
    else:
        products = Product.objects.all().order_by('-created_date')
    context = {'products': products, 'products_count': len(
        products)}

    return render(request, 'store/store.html', context)


def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    current_user = request.user
    if request.method == 'POST':
        # Updating the existing review
        if ReviewRating.objects.filter(user__id=current_user.id, product__id=product_id).exists():
            review = ReviewRating.objects.get(
                user__id=request.user.id, product__id=product_id)
            product = Product.objects.get(id=product_id)
            product.total_ratings_sum -= review.rating
            form = ReviewForm(request.POST, request.FILES, instance=review)
            form.save()
            review = ReviewRating.objects.get(
                user__id=request.user.id, product__id=product_id)
            product.total_ratings_sum += review.rating
            product.average_rating = product.total_ratings_sum/product.total_reviews
            product.save()
            messages.success(request, 'Thank you for your form update!')
            return redirect(url)
        else:
            form = ReviewForm(request.POST, request.FILES)
            if form.is_valid():
                data = ReviewRating()
                data.review_title = form.cleaned_data['review_title']
                data.review_description = form.cleaned_data['review_description']
                data.rating = form.cleaned_data['rating']
                data.review_image = form.cleaned_data['review_image']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                product = Product.objects.get(id=product_id)
                product.total_reviews += 1
                product.total_ratings_sum += data.rating
                product.average_rating = product.total_ratings_sum/product.total_reviews
                product.save()
                messages.success(
                    request, 'Thank you for your form submission!')
                return redirect(url)
            pass
    return redirect('home')
