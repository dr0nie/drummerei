from django.urls import path

from ninja import NinjaAPI

from .views.schedules import router as schedule_router
from .views.slots import router as slot_router

app = NinjaAPI()
app.add_router("/schedules", schedule_router)
app.add_router("/schedules/", slot_router)

urlpatterns = [
    path('', app.urls),
]
