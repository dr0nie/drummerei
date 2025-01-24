from django.urls import path
from django.views.generic.base import RedirectView

from .views import home,schedule

urlpatterns = [
    path('', home),
    path('<str:date>/', schedule),
]
