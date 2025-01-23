from random import randint
from datetime import time, timedelta, datetime
from uuid import UUID,uuid4
import qrcode

from django.db import models

class Settings(models.Model):
    """
    Application settings.

    This model is used to store various configuration settings for the application.
    It includes fields for title, subtitle, URL, default QR code path, start time,
    duration, and slot duration. The settings are loaded or created with a fixed
    primary key to ensure a singleton pattern.

    Attributes:
        title (str): The title of the application.
        subtitle (str): A subtitle for the application.
        url (str): The URL associated with the application.
        default_qr_code_path (str): The default path for storing QR code images.
        default_start_time (time): The default start time for slots.
        default_duration (timedelta): The default duration for schedules.
        default_slot_duration (timedelta): The default duration for individual slots.
    """

    class Meta:
        verbose_name_plural = "Settings"

    title = models.CharField(
        max_length=255,
        default="Drummerei",
        help_text="The title of the application."
    )
    subtitle = models.CharField(
        max_length=255,
        default="Open Decks Timetable",
        help_text="A subtitle for the application."
    )
    url = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="The URL associated with the application."
    )
    default_qr_code_path = models.CharField(
        max_length=255,
        default="drummerei/static/image/qr.png",
        help_text="The default path for storing QR code images."
    )
    default_start_time = models.TimeField(
        default=time(20, 0),
        help_text="The default start time for slots."
    )
    default_duration = models.DurationField(
        default=timedelta(hours=4),
        help_text="The default duration for schedules."
    )
    default_slot_duration = models.DurationField(
        default=timedelta(minutes=30),
        help_text="The default duration for individual slots."
    )
    @classmethod
    def load(cls):
        """
        Loads or creates the settings instance.

        This class method ensures that the settings instance is loaded or created
        with a fixed primary key to maintain a singleton pattern.
        Returns:
            Settings: The settings instance.
        """
        obj, _ = cls.objects.get_or_create(id=1)
        return obj
    
    def save(self, *args, **kwargs):
        """
        Saves the settings instance.

        Overrides the default save method to ensure the settings instance always
        has a fixed primary key, maintaining a singleton pattern.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        self.pk = 1
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        """
        Returns the string representation of the settings instance.
        Returns:
            str: The title of the settings instance.
        """
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
    """
    Represents a time slot.

    This model stores information about a time slot, including its name, start time, 
    and unique identifier.

    Attributes:
        name (str): The name of the slot.
        start_time (time): The start time of the slot.
        slot_id (UUID): A unique identifier for the slot.
    """

    name = models.CharField(max_length=255,null=True)
    start_time = models.TimeField(default=generate_start_time)
    slot_id = models.UUIDField(null=True, blank=True)

    def reserve(self, name: str) -> UUID:
        """
        Reserves the slot with the given name and generates a unique identifier.

        This method updates the name of the slot with the provided value and 
        generates a unique identifier for the slot. The changes are then saved to 
        the database.
        Args:
            name (str): The name to assign to the slot.
        Returns:
            UUID: The unique identifier for the slot.
        """
        self.name = name
        self.slot_id = uuid4()
        self.save()
        return self.slot_id

    def clear_slot_with_id(self, slot_id: UUID):
        """
        Clears the unique identifier and name for the slot with the given ID.

        This method checks if the given slot_id matches the slot's ID, and if so,
        resets the name and slot_id to None, effectively clearing the slot.
        The changes are then saved to the database.

        Args:
            slot_id (UUID): The ID of the slot to clear.

        Returns:
            None
        Raises:
            ValueError: If the slot ID does not match the current slot's ID.
        """
        if self.slot_id == slot_id:
            self.clear_slot()
            self.save()
        else:
            raise ValueError("Slot ID does not match")
        
    def clear_slot(self):
        """
        Clears the unique identifier and name for the slot.

        This method resets the name and slot_id to None, effectively clearing the slot.
        The changes are then saved to the database.

        Returns:
            None
        """
        self.name = None
        self.slot_id = None
        self.save()

    def __str__(self) -> str:
        """
        Returns the string representation of the slot.

        The string representation includes the schedule, start time, and name of the slot.

        Returns:
            str: The string representation of the slot.
        """
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
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def save(self):
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
            super().save()            
            self.slots.add(*self.__generate_slots())
        else:
            schedules = list(self.__class__.objects.filter(id=self.id))
            old_schedule = schedules[0]
            oldpin = old_schedule.pin
            if self.pin != oldpin:
                self.generate_qrcode(qrcode_path)

        return super().save()

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
        return f"{Settings.load().url}?pin={self.pin}"

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
                    datetime.combine(
                        datetime(1, 1, 1),
                        Settings.load().default_start_time
                    ) + timedelta(minutes=i * 30)
                ).time()
            )
            slot.save()
            slots.append(slot)
        return slots
