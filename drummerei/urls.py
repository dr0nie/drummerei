from django.urls import path

from .views import home,schedule

urlpatterns = [
    path('', home),
    #TODO: only handle formated date strings
    path('<str:date>', schedule),
]
