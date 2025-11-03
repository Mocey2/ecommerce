from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('contact/', include('contact.urls')),
    path('about/', include('about.urls')),
    path('produits/', include('produit.urls')),
    path('blog/', include('blog.urls')),
    path('authentification/', include('authentification.urls')),
    path('', include('accueil.urls')),
    path('base/', include('base.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


