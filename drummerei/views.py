import uuid

from django.shortcuts import render
from django.http import HttpResponse

from .models import Schedule, Settings

def home(request) -> HttpResponse:
    context = {
        'schedules': Schedule.objects.all(),
    }
    return render(request, 'pages/dates.html', context)


def create_context_for_schedule(date:str,pin:str,slotId:uuid.UUID) -> dict:
    context = {
        "kiosk":True,
        # "range_add_slots":range(2),
        "slot_id_from_cookies":slotId,
        "site":Settings.load()
    }

    schedules = list(Schedule.objects.filter(start_time__date=date))
    if len(schedules)==1:
        context['schedule']=schedules[0]

        delta = schedules[0].end_time - schedules[0].start_time
        # context["range_slots_left"] = range(int(delta.seconds/60/30) - 4) # simulate four elapsed slots

    if pin:
        if pin.isnumeric():
            context["kiosk"] = int(pin) != context["schedule"].pin

    return context


def schedule(request,date:str) -> HttpResponse:

    slotId = request.COOKIES.get('drummerei_slotId')   
    if not slotId:
        slotId = uuid.uuid4()

    context = create_context_for_schedule(date,request.GET.get("pin"),slotId)

    response = render(request, 'pages/schedule.html', context)
    response.set_cookie('drummerei_slotId', slotId)

    return response
