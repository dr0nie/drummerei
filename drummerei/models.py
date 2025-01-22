from random import randint
from datetime import time, timedelta, datetime
import qrcode

from django.db import models

class Settings(models.Model):
    class Meta:
        verbose_name_plural = "Settings"

    title = models.CharField(max_length=255,default="Drummerei")
    subtitle = models.CharField(max_length=255,default="Open Decks Timetable")
    url = models.CharField(max_length=255,null=True,blank=True)

    default_start_time = models.TimeField(default=time(20,0))
    default_duration = models.DurationField(default=timedelta(hours=4))
    default_slot_duration = models.DurationField(default=timedelta(minutes=30))

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(id=1)
        return obj
    
    def save(self,*args, **kwargs):
        self.pk=1
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title


def generate_start_time() -> time:
    """
    Retrieves the default start time from the Settings model.

    This function loads the settings and returns the default start time specified
    in the Settings model. It is used to initialize time-related fields with a 
    predefined default value.

    Returns:
        time: The default start time as specified in the Settings model.
    """
    return Settings.load().default_start_time


class Slot(models.Model):
    name = models.CharField(max_length=255)
    start_time = models.TimeField(default=generate_start_time)
    slot_id = models.UUIDField(null=True,blank=True)

    def __str__(self) -> str:
        schedule = None
        all_schedules = Schedule.objects.all()
        if all_schedules.exists():
            schedule = all_schedules.first()
        return f"{schedule} @ {self.start_time}: {self.name}"

def generate_pin() -> int:
    """
    Generates a random 4-digit pin.

    This function generates a random integer between 1000 and 9999 to be used
    as a pin.

    Returns:
        int: A randomly generated 4-digit pin.
    """
    pin = randint(1000,9999)
    return pin

class Schedule(models.Model):
    slots = models.ManyToManyField(Slot,editable=False)
    pin = models.IntegerField(default=generate_pin)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def save(self):
        #TODO: put qrcode path in Settings
        qrcode_path = "drummerei/static/image/qr.png"
        if self.id is None:
            self.generate_qrcode(qrcode_path)
            super().save()            
            self.slots.add(*self.__generate_slots())

        else:
            schedules=list(self.__class__.objects.filter(id=self.id))
            old_schedule = schedules[0]
            oldpin = old_schedule.pin
            if self.pin != oldpin:
                self.generate_qrcode(qrcode_path)

        return super().save()

    def delete(self):
        for slot in list(self.slots.all()):
            slot.delete()
        super().delete()

    def generate_url_with_pin(self):
        return f"{Settings.load().url}?pin={self.pin}"

    def generate_qrcode(self,path:str):
        data = self.generate_url_with_pin()
        img = qrcode.make(data)
        img.save(path)

    def __str__(self) -> str:
        return str(self.start_time.date())
    
    def __generate_slots(self) -> list[Slot]:
        number_of_slots = int(
            Settings.load().default_duration.total_seconds() / Settings.load().default_slot_duration.total_seconds()
        )
        slots = []
        for i in range(number_of_slots):
            slot = Slot(
                    start_time=(
                        datetime.combine(
                            datetime(1,1,1),
                            Settings.load().default_start_time
                        ) + timedelta(minutes=i*30)
                        ).time()
                    )
            slot.save()
            slots.append(slot)
        return slots
