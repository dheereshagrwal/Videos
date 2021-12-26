
from django.urls import path
from . import views
urlpatterns = [
    path('', views.store, name='store'),
    path('<slug:category_or_subcategory_slug>/', views.store,
         name='products_by_category_or_subcategory'),
    path('<slug:category_or_subcategory_slug>/<slug:product_slug>/', views.product_details,
         name='product_details'),

]
