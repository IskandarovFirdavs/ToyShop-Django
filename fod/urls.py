from django.contrib import admin
from django.urls import path, include
from fod import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls', namespace='users')),
    path('', include('products.urls', namespace='products')),
    path('contact/', include('contact.urls', namespace='contact')),
    ]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
