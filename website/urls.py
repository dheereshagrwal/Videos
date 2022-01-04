
from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView

urlpatterns = [
    # path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('store/', include('store.urls')),
    path('cart/', include('cart.urls')),
    # path('accounts/', include('django.contrib.auth.urls')),
    path('order/', include('order.urls')),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('my_orders/', views.my_orders, name='my_orders'),
    path('order_details/<int:order_id>/',
         views.order_details, name='order_details'),

    path('accounts/', include('allauth.urls')),
    path('login/', TemplateView.as_view(template_name="account/login.html")),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
