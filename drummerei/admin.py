from django.contrib import admin
from .models import Slot, Schedule, Settings

class SlotAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_time', 'get_schedule')

    def get_schedule(self, obj):
        return obj.schedule_set.all().first()
    get_schedule.short_description = 'Schedule'
    

class ScheduleAdmin(admin.ModelAdmin):
    # list_display = ('name', 'start_time', 'get_schedule')
    filter_horizontal = ('slots',)

    
admin.site.register(Slot,SlotAdmin)
admin.site.register(Schedule,ScheduleAdmin)
admin.site.register(Settings)