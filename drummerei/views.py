import datetime
import uuid

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from .models.settings import Settings
from .models.schedule import Schedule

def home(request) -> HttpResponse:
    context = {
        'schedules': Schedule.objects.all(),
    }
    return render(request, 'pages/dates.html', context)


def create_context_for_schedule(date:str,pin:str,slotId:uuid.UUID) -> dict:
    now =  datetime.datetime.now() + datetime.timedelta(hours=Settings.load().unlock_hours)
    context = {
        "kiosk":True,
        # "range_add_slots":range(2),
        "slot_id_from_cookies":slotId,
        "site":Settings.load(),
        # "now":datetime.datetime.now() + datetime.timedelta(hours=1)
        "now":datetime.time(hour=now.hour,minute=now.minute)
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

def clear_slot(request,date:str,slot_id:int) -> HttpResponse:
    schedule = Schedule.objects.get(start_time__date=date)
    slot = schedule.slots.get(id=slot_id)
    slot.name = None
    slot.slot_id = None
    slot.save()
    return HttpResponseRedirect(
        redirect_to=f"/{date}?pin={request.POST.get("pin")}"
    )

def reserve_slot(request,date:str,slot_id:int) -> HttpResponse:
    schedule = Schedule.objects.get(start_time__date=date)
    slot = schedule.slots.get(id=slot_id)
    slot.name = request.POST.get("name")
    slot.slot_id = request.COOKIES.get('drummerei_slotId')
    slot.save()
    return HttpResponseRedirect(
        redirect_to=f"/{date}?pin={request.POST.get("pin")}"
    )