from random import randint
from datetime import time, timedelta,datetime
from typing import Iterable, Optional
from django.db import models
import qrcode


def generate_start_time():
    return Settings.load().default_start_time

class Slot(models.Model):
    name = models.CharField(max_length=255)
    start_time = models.TimeField(default=generate_start_time)
    slot_id = models.UUIDField(null=True,blank=True)

    def __str__(self) -> str:
        return f"{self.schedule_set.all().first()} @ {self.start_time}: {self.name}"

def generate_qrcode(pin:int):
    data = f"https://{Settings.load().url}?pin={pin}"
    img = qrcode.make(data)
    img.save("drummerei/static/image/qr.png")

def generate_pin() -> int:
    pin = randint(1000,9999)
    generate_qrcode(pin)
    return pin

def generate_slots():
    number_of_slots = int(
        Settings.load().default_duration.total_seconds() / Settings.load().default_slot_duration.total_seconds()
    )
    slots = []
    for i in range(number_of_slots):
        slot = Slot(
                start_time=(
                    datetime.combine(
                        datetime(1,1,1),
                        generate_start_time()
                    ) + timedelta(minutes=i*30)
                    ).time()
                )
        slot.save()
        slots.append(slot)
    return slots

#TODO: use signals after save
class Schedule(models.Model):
    slots = models.ManyToManyField(Slot,default=generate_slots,null=True,blank=True)
    pin = models.IntegerField(default=generate_pin)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def delete(self):
        for slot in list(self.slots.all()):
            slot.delete()
        super().delete()

    def save(self):
        schedules=list(self.__class__.objects.filter(id=self.id))
        if len(schedules) == 1:
            old_schedule = schedules[0]
            oldpin = old_schedule.pin
            if self.pin != oldpin:
                generate_qrcode(self.pin)
        super().save()

    def __str__(self) -> str:
        return str(self.start_time.date())

class Settings(models.Model):
    class Meta:
        verbose_name_plural = "Settings"

    title = models.CharField(max_length=255,default="Drummerei")
    subtitle = models.CharField(max_length=255,default="Open Decks Timetable")
    url = models.CharField(max_length=255,null=True,blank=True)

    default_start_time = models.TimeField(default=time(20,0))
    default_duration = models.DurationField(default=timedelta(hours=4))
    default_slot_duration = models.DurationField(default=timedelta(minutes=30))

    def save(self,*args, **kwargs):
        self.pk=1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(id=1)
        return obj
    
    def __str__(self) -> str:
        return self.title