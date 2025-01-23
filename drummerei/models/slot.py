from datetime import time
from uuid import UUID,uuid4

from django.db import models

from .settings import Settings


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
        all_schedules = self.schedule_set.all()
        if all_schedules.exists():
            schedule = all_schedules.first()
        return f"{schedule} @ {self.start_time}: {self.name}"