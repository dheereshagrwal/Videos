
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views
urlpatterns = [
    path('', views.store, name='store'),
    path('view/<slug:category_slug>/', views.store,
         name='products_by_category'),
    path('view/<slug:category_slug>/<slug:subcategory_slug>/', views.store,
         name='products_by_subcategory'),
    path('view/<slug:category_slug>/<slug:subcategory_slug>/<slug:product_slug>/', views.product_details,
         name='product_details'),
    path('submit_review/<int:product_id>/',
         views.submit_review, name='submit_review')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
