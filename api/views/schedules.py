from django.shortcuts import get_object_or_404

from ninja import ModelSchema, Router
from typing import List

from drummerei.models.schedule import Schedule

router = Router(tags=["Resources"],)

class ScheduleSchema(ModelSchema):
    class Config:
        title= "Schedule"
        model = Schedule
        model_fields = "__all__"


@router.get("", response=List[ScheduleSchema])
def get_all_schedules(request):
    schedules = Schedule.objects.all()
    return list(schedules)

@router.get("{schedule_id}", response=ScheduleSchema)
def get_schedule_by_id(request, schedule_id: int):
    schedule = get_object_or_404(Schedule, pk=schedule_id)
    return schedule
