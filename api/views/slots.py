from typing import List, Optional
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from ninja import ModelSchema, Router, Schema

from drummerei.models.schedule import Schedule
from drummerei.models.slot import Slot

router = Router(tags=["Resources"])


class PinSchema(Schema):
    class Config:
        title= "PIN"
    pin: Optional[int] = None

class ReservationSchema(PinSchema):
    class Config:
        title= "Reservation"
    name: str

class SlotSchema(ModelSchema):
    class Config:
        title= "Slot"
        model = Slot
        model_fields = "__all__"
    pin: Optional[int] = None


@router.get("{schedule_id}/slots",response=List[SlotSchema])
def get_all_slots(request, schedule_id: int):
    schedule = get_object_or_404(Schedule, pk=schedule_id)
    return list(schedule.slots.all())

@router.get("{schedule_id}/slots/{slot_id}",response=SlotSchema)
def get_slot_by_id(request, schedule_id: int, slot_id: int):
    schedule = get_object_or_404(Schedule, pk=schedule_id)
    slot = schedule.slots.get(pk=slot_id)
    return slot

@router.patch("{schedule_id}/slots/{slot_id}/reserve",response=SlotSchema)
def reserve_slot_with_id(request, schedule_id: int, slot_id: int, payload:ReservationSchema):
    schedule = get_object_or_404(Schedule, pk=schedule_id)
    if schedule.pin == payload.pin:
        #name = request.PATCH.get("name")
        name = payload.name
        slot = schedule.slots.get(pk=slot_id)
        slot.name = name
        slot.save()
        return slot
    else:
        return JsonResponse({"error": "Invalid PIN"}, status=401)

@router.patch("{schedule_id}/slots/{slot_id}/clear",response=SlotSchema)
def clear_slot_with_id(request, schedule_id: int, slot_id: int, payload:PinSchema):
    schedule = get_object_or_404(Schedule, pk=schedule_id)
    if schedule.pin == payload.pin:
        slot = schedule.slots.get(pk=slot_id)
        slot.name = None
        slot.save()
        return slot
    else:
        return JsonResponse({"error": "Invalid PIN"}, status=401)
