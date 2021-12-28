
from django.urls import path
from . import views
urlpatterns = [
    path('', views.store, name='store'),
    path('category_or_subcategory/<slug:category_or_subcategory_slug>/', views.store,
         name='products_by_category_or_subcategory'),
    path('category_or_subcategory/<slug:category_or_subcategory_slug>/<slug:product_slug>/', views.product_details,
         name='product_details'),
    path('search/', views.search, name='search'),
    path('filter_by_anime/', views.filter_by_anime, name='filter_by_anime'),
]
