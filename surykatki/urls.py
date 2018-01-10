from django.urls import include, path
from django.conf import settings

# Funkcja static działa tylko jeśli DEBUG jest False
from django.conf.urls.static import static

# Moduł administracji nie jest potrzebny
# from django.contrib import admin

urlpatterns = [
    path('', include('stronka.urls')),
    # path('admin/', admin.site.urls),
]

# Serwowanie plików z folderu media
if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
