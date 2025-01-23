
from django.contrib import admin
from django.urls import path,include

from django.conf import settings
from django.conf.urls.static import static

from drummerei.urls import urlpatterns as drummerei_urls

urlpatterns = [
    path('admin/doc/', include(
        'django.contrib.admindocs.urls'
    )),
    path('admin/', admin.site.urls),
    path('', include(drummerei_urls)),
] + static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT
    )
