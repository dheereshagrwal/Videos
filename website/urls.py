
from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('store/', include('store.urls')),
    path('cart/', include('cart.urls')),
    # path('accounts/login/',views.login,name='login'),
    # path('accounts/register/', views.register, name='register'),
    # path('accounts/logout/', views.logout, name='logout'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('dashboard/', views.dashboard, name='dashboard'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
