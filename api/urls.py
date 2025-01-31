from django.urls import path

from ninja import NinjaAPI

from .views.schedules import router as schedule_router
from .views.slots import router as slot_router

app = NinjaAPI(
    title="drummerei API",
    version="0.1.0",
    description="API for the drummerei app.",
    servers=[
        { "url": "http://localhost:8000" },
    ],
    openapi_extra={
       "info": {
           "termsOfService": "",
       }
   },
)

app.add_router("/schedules", schedule_router)
app.add_router("/schedules/", slot_router)

urlpatterns = [
    path('', app.urls),
]
