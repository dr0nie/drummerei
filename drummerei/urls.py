from django.urls import path

from .views import (
    home,
    schedule,
    clear_slot,
    reserve_slot,
)

urlpatterns = [
    path('', home),
    #FIXME: favicon.ico is not found, only read date strings here
    path('<str:date>/', schedule),
    path('<str:date>/slots/<int:slot_id>/clear', clear_slot),
    path('<str:date>/slots/<int:slot_id>/reserve', reserve_slot),
]
