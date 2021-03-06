from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404, HttpResponse
from . models import Product, ProductImages
from review.models import ReviewRating, ReviewImage
from review.forms import ReviewForm, ReviewFullForm
from category.models import Category
from subcategory.models import Subcategory
from cart.views import _get_cart_id
from cart.models import Cart, CartItem
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.contrib import messages
from order.models import OrderProduct


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
                    category=category, subcategory=subcategory, is_available=True).order_by('-created_date')
            # If there is only category
            else:
                products = Product.objects.filter(
                    category=category, is_available=True).order_by('-created_date')
            paginator = Paginator(products, 9)
            page = request.GET.get('page')
            paged_products = paginator.get_page(page)
            products_count = products.count()
            context = {'products': paged_products,
                       'products_count': products_count}
        except:
            raise Http404("Given query not found....")

    else:
        sort_by = '-created_date'
        for sort_category in request.GET.getlist('sort_by'):
            # '-' is added because we want in decreasing order
            if sort_category == "price":
                sort_by = 'price'
            else:
                sort_by = '-' + sort_category

        is_categories = False
        is_subcategories = False
        is_animes = False
        categories = request.GET.getlist('category_filter')
        subcategories = request.GET.getlist('subcategory_filter')
        animes = request.GET.getlist('anime_filter')
        if categories:
            is_categories = True
        if subcategories:
            is_subcategories = True
        if animes:
            is_animes = True
        if is_categories and (not is_subcategories):
            # This is products list not to be confused with products
            if is_animes:
                products = []
                for category in categories:
                    for anime in animes:
                        for item in Product.objects.filter(category__category_name=category, anime__slug=anime, is_available=True):
                            products.append(item)
                products_count = len(products)
            if not is_animes:
                products = []
                for category in categories:
                    for item in Product.objects.order_by(sort_by).filter(category__category_name=category, is_available=True):
                        products.append(item)
                products_count = len(products)
        # Only subcategories exist but not categories, this is possible during filter,so redirect to store page
        if is_subcategories and not(is_categories):
            return redirect('store')

        # Both subcategories and categories exist
        if is_subcategories and is_categories:
            if is_animes:
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
                        for item in Product.objects.filter(category__category_name=cat_, is_available=True):
                            products.append(item)
                    else:
                        for subcat_ in filter_dict[cat_]:
                            for anime in animes:
                                for item in Product.objects.filter(category__category_name=cat_, subcategory__subcategory_name=subcat_, anime__slug=anime, is_available=True):
                                    products.append(item)
                products_count = len(products)
            if not is_animes:
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
                        for item in Product.objects.filter(category__category_name=cat_, is_available=True):
                            products.append(item)
                    else:
                        for subcat_ in filter_dict[cat_]:
                            for item in Product.objects.filter(category__category_name=cat_, subcategory__subcategory_name=subcat_, is_available=True):
                                products.append(item)
                products_count = len(products)

        # On store page, only anime are ticked
        if (not is_categories) and (not is_subcategories) and (is_animes):
            products = []
            for anime in animes:
                for item in Product.objects.filter(anime__slug=anime, is_available=True):
                    products.append(item)
            products_count = len(products)
        # *Implement sort here

        def get_sort_by(product):
            return getattr(product, 'price') if sort_by == 'price' else getattr(product, sort_by[1:])
        if products:
            products.sort(key=get_sort_by) if sort_by == 'price' else products.sort(
                key=get_sort_by, reverse=True)
            products_count = len(products)
        # * Getting all the products when in store and using the default sort

        if (not is_categories) and (not is_subcategories) and (not is_animes):
            products = Product.objects.all().order_by(sort_by).filter(is_available=True)
            products_count = products.count()

        if 'keyword' in request.GET:
            keyword = request.GET['keyword']
            request.session['keyword'] = keyword
        try:
            page_number = request.GET.get('page')
            if not page_number:
                page_number = 1
            if is_categories or is_subcategories or is_animes or request.get_full_path() == '/store/' or page_number > 1:
                keyword = ""
            else:
                keyword = request.session['keyword']
                products = search(keyword, sort_by)
                products.sort(key=get_sort_by) if sort_by == 'price' else products.sort(
                    key=get_sort_by, reverse=True)
                products_count = len(products)
        except:
            keyword = ""
        paginator = Paginator(products, 10)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        context = {'products': paged_products,
                   'products_count': products_count, 'keyword': keyword, }

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
    images = []
    for review in reviews:
        images.append(ReviewImage.objects.filter(review_rating=review))
    zipped_reviews=zip(reviews,images) 
    # Get the product images
    product_images = ProductImages.objects.filter(product_id=single_product.id)
    context = {'single_product': single_product, 'in_cart': in_cart,
               'orderproduct': orderproduct, 'zipped_reviews': zipped_reviews, 'product_images': product_images,}
    return render(request, 'store/product-details.html', context)


def search(keyword, sort_by):
    products = []
    keyword = keyword.lower()
    keywords = keyword.split(' ')
    for key in keywords:
        for item in Product.objects.order_by(sort_by).filter(Q(product_description__icontains=key) | Q(product_name__icontains=key) | Q(anime__anime_name__icontains=key) | Q(anime__slug__icontains=key) | Q(anime__anime_description__icontains=key) | Q(category__category_name__icontains=key) | Q(subcategory__subcategory_name__icontains=key) | Q(category__slug__icontains=key) | Q(subcategory__slug__icontains=key) | Q(category__category_description__icontains=key) | Q(subcategory__subcategory_description__icontains=key)):
            products.append(item)
    products = list(set(products))
    return products

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
            form = ReviewFullForm(request.POST, request.FILES, instance=review)
            form.save()
            review = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            if request.FILES.getlist('images'):
                ReviewImage.objects.filter(review_rating=review).delete()
                files = request.FILES.getlist('images')
                for f in files: 
                    ReviewImage.objects.update_or_create(review_rating=review, image=f)
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
                # data.review_image = form.cleaned_data['review_image']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                if request.FILES.getlist('images'):
                    files = request.FILES.getlist('images')
                    for f in files:
                        ReviewImage.objects.create(review_rating=data, image=f)
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
