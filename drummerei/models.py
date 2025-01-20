from typing import Iterable, Optional
from django.db import models
from random import randint
import qrcode

class Slot(models.Model):
    name = models.CharField(max_length=255)
    time = models.DateTimeField()
    slot_id = models.UUIDField(null=True,blank=True)

    def __str__(self) -> str:
        return self.name

def generate_qrcode(pin:int):
    data = f"https://{Settings.load().url}?pin={pin}"
    img = qrcode.make(data)
    img.save("drummerei/static/image/qr.png")

def generate_pin() -> int:
    pin = randint(1000,9999)
    generate_qrcode(pin)
    return pin

class Schedule(models.Model):
    slots = models.ManyToManyField(Slot,null=True,blank=True)
    pin = models.IntegerField(default=generate_pin)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def save(self):
        generate_qrcode(self.pin)
        super().save()

    def __str__(self) -> str:
        return str(self.start_time.date())

class Settings(models.Model):
    class Meta:
        verbose_name_plural = "Settings"

    title = models.CharField(max_length=255,default="Drummerei")
    subtitle = models.CharField(max_length=255,null=True,blank=True)
    url = models.CharField(max_length=255,null=True,blank=True)

    def save(self,*args, **kwargs):
        self.pk=1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(id=1)
        return obj
    
    def __str__(self) -> str:
        return self.title