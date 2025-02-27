import datetime
import uuid

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

from drummerei.forms import ReserveSlotForm

from .models.settings import Settings
from .models.schedule import Schedule

def home(request) -> HttpResponse:
    context = {
        'schedules': Schedule.objects.all(),
    }
    return render(request, 'pages/dates.html', context)


def create_context_for_schedule(date:str,pin:str,slotId:uuid.UUID) -> dict:
    now =  datetime.datetime.now() + datetime.timedelta(hours=get_object_or_404(Schedule,start_time__date=date).unlock_hours)
    context = {
        "kiosk":True,
        # "range_add_slots":range(2),
        "slot_id_from_cookies":slotId,
        "site":Settings.load(),
        # "now":datetime.datetime.now() + datetime.timedelta(hours=1)
        "now":datetime.time(hour=now.hour,minute=now.minute),
        "schedule":get_object_or_404(Schedule,start_time__date=date),
    }

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

def edit_slot(request,date:str,slot_id:int) -> HttpResponse|JsonResponse:
    schedule = get_object_or_404(Schedule,start_time__date=date)
    form = ReserveSlotForm(request.POST)
    if form.is_valid():
        if schedule.pin == form.cleaned_data["pin"]:
            if request.POST.get("clear"):
                slot = schedule.slots.get(id=slot_id)
                slot.name = None
                slot.slot_id = None
                slot.save()
            if request.POST.get("update"):
                slot = schedule.slots.get(id=slot_id)
                slot.name = request.POST.get("name")
                slot.save()
            return HttpResponseRedirect(
                redirect_to=f"/{date}?pin={request.POST.get("pin")}"
            )
    else:
        return JsonResponse({"error": "Invalid PIN"}, status=401)

def reserve_slot(request,date:str,slot_id:int) -> HttpResponse|JsonResponse:
    form = ReserveSlotForm(request.POST)
    if form.is_valid():
        schedule = get_object_or_404(Schedule,start_time__date=date)
        if schedule.pin == form.cleaned_data["pin"]:
            slot = schedule.slots.get(id=slot_id)
            slot.name = request.POST.get("name")
            slot.slot_id = request.COOKIES.get('drummerei_slotId')
            slot.save()
            return HttpResponseRedirect(
                redirect_to=f"/{date}?pin={request.POST.get("pin")}"
            )
        else:
            return JsonResponse({"error": "Invalid PIN"}, status=401)
    else:
        return JsonResponse({"error": "Invalid form data"}, status=400)
