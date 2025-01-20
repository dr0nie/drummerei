from django.contrib import admin
from .models import Slot, Schedule, Settings

admin.site.register(Slot)
admin.site.register(Schedule)
admin.site.register(Settings)