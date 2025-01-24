from django.urls import path
from django.views.generic.base import RedirectView

from .views import home,schedule

urlpatterns = [
    path('', home),
    #FIXME: favicon.ico is not found, only read date strings here
    path('<str:date>/', schedule),
]
