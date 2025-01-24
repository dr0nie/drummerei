from datetime import time, timedelta

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
        default="http://druckse/ledwand",
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
