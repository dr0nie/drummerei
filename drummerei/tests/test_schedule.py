from datetime import datetime, timedelta

from django.test import TestCase

from ..models.settings import Settings
from ..models.schedule import Schedule, generate_pin

class HelperFunctionsTest(TestCase):
    def test_generate_pin(self):
        self.assertTrue(1000 <= generate_pin() <= 9999 ) # ! pin is RANDOM
        
class ScheduleModelTest(TestCase):
    def setUp(self):
        self.start_time = datetime.now()
        self.end_time=self.start_time + timedelta(hours=4)

        self.settings = Settings.load()
        self.settings.default_qr_code_path = "drummerei/static/image/test.png"
        self.settings.url = "http://localhost:8000"
        self.settings.save()
        self.schedule = Schedule.objects.create(
            start_time=self.start_time,
            end_time=self.end_time,
        )

    def test_creation(self):
        self.assertEqual(self.schedule.start_time, self.start_time)
        self.assertEqual(self.schedule.end_time, self.end_time )
        self.assertTrue(isinstance(self.schedule, Schedule))

        self.assertTrue(0 < len(self.schedule.slots.all())  )
        
        self.assertEqual(str(self.schedule), str(self.schedule.start_time.date()))

    def test_generate_url_with_pin(self):
        self.assertEqual(
            self.schedule.generate_url_with_pin(),
            f"{self.settings.url}/{self.schedule}?pin={self.schedule.pin}"
        )

    def test_generate_qrcode(self):
        from PIL import Image
        from pyzbar import pyzbar

        img = Image.open(Settings.load().default_qr_code_path)
        output = pyzbar.decode(img)[0].data.decode("utf-8")
        self.assertEqual(output, self.schedule.generate_url_with_pin())
