from django.urls import path

from .views import home,schedule

urlpatterns = [
    path('', home),
    path('<str:date>', schedule),
]
