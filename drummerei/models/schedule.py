from random import randint
from datetime import timedelta, datetime,time
import qrcode

from django.db import models

from .settings import Settings
from .slot import Slot


def generate_start_time() -> datetime:
    today = datetime.today()
    start = datetime.combine(today, Settings.load().default_start_time)
    return start

def generate_end_time() -> datetime:
    return generate_start_time() + Settings.load().default_duration


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

def generate_unlock_hours() -> int:
    return Settings.load().default_unlock_hours

class Schedule(models.Model):
    """
    Represents a schedule containing multiple slots.

    This model defines a schedule with slots, a unique pin, a start time, and an end time.
    It also provides methods to generate a QR code, manage slots, and handle URL generation
    with a pin for the schedule.

    Attributes:
        slots (ManyToManyField): A many-to-many relationship with the Slot model.
        pin (IntegerField): A randomly generated 4-digit pin for the schedule.
        start_time (DateTimeField): The start time of the schedule.
        end_time (DateTimeField): The end time of the schedule.
    """
    slots = models.ManyToManyField(Slot, editable=False)
    pin = models.IntegerField(default=generate_pin)
    start_time = models.DateTimeField(default=generate_start_time)
    end_time = models.DateTimeField(default=generate_end_time)
    unlock_hours = models.IntegerField(default=generate_unlock_hours)

    def save(self, *args, **kwargs):
        """
        Saves the schedule instance.

        Overrides the default save method to generate a QR code and associate slots
        with the schedule. If the schedule is new, it generates slots and a QR code.
        If the pin changes, it regenerates the QR code.

        Returns:
            None
        """
        qrcode_path = Settings.load().default_qr_code_path
        if self.id is None:
            self.generate_qrcode(qrcode_path)
            super().save(*args, **kwargs)
            self.slots.add(*self.__generate_slots())
        else:
            schedules = list(self.__class__.objects.filter(id=self.id))
            old_schedule = schedules[0]
            if self.pin != old_schedule.pin:
                self.generate_qrcode(qrcode_path)

            if self.end_time != old_schedule.end_time:
                #TODO: update slots
                pass
            super().save(*args, **kwargs)

    def delete(self):
        """
        Deletes the schedule instance.

        Overrides the default delete method to remove all associated slots
        before deleting the schedule itself.

        Returns:
            None
        """
        for slot in list(self.slots.all()):
            slot.delete()
        super().delete()

    def generate_url_with_pin(self) -> str:
        """
        Generates a URL with the schedule's pin.

        Constructs a URL using the base URL from the Settings model and appends
        the schedule's pin as a query parameter.

        Returns:
            str: The generated URL with the pin.
        """
        return f"{Settings.load().url}/{self}?pin={self.pin}"

    def generate_qrcode(self, path: str):
        """
        Generates a QR code for the schedule.

        Creates a QR code containing the URL with the schedule's pin and saves
        it to the specified path.

        Args:
            path (str): The file path where the QR code image will be saved.

        Returns:
            None
        """
        data = self.generate_url_with_pin()
        img = qrcode.make(data)
        img.save(path)

    def __str__(self) -> str:
        """
        Returns the string representation of the schedule instance.

        Returns:
            str: The date part of the schedule's start time.
        """
        return str(self.start_time.date())
    
    def __generate_slots(self) -> list[Slot]:
        """
        Generates slots for the schedule.

        Uses the default duration and slot duration from the Settings model to
        create and save individual Slot instances for the schedule.

        Returns:
            list[Slot]: A list of generated Slot instances.
        """
        number_of_slots = int(
            Settings.load().default_duration.total_seconds() / Settings.load().default_slot_duration.total_seconds()
        )
        slots = []
        for i in range(number_of_slots):
            slot = Slot(
                start_time=(
                    self.start_time
                    # datetime.combine(
                    #     datetime(1, 1, 1),
                    #     Settings.load().default_start_time
                    # )
                      + timedelta(minutes=i * 30)
                ).time()
            )
            slot.save()
            slots.append(slot)
        return slots
