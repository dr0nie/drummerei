from django.contrib import admin
from django.urls import path,include
from django.views.generic.base import RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/doc/', include(
        'django.contrib.admindocs.urls'
    )),
    path('admin', RedirectView.as_view(url='admin/')),
    path('admin/', admin.site.urls),
    path('', include('drummerei.urls')),
] + static(
    settings.STATIC_URL,
    document_root=settings.STATIC_ROOT
)
