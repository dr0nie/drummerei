from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('api/', include("api.urls")),
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls),
    path('', include('drummerei.urls')),
] + static(
    settings.STATIC_URL,
    document_root=settings.STATIC_ROOT
)
