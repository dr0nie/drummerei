from datetime import datetime, timedelta

from django.test import TestCase

from .models.settings import Settings
from .models.slot import Slot, generate_start_time
from .models.schedule import Schedule, generate_pin

class HelperFunctionsTest(TestCase):
    def test_generate_pin(self):
        self.assertTrue(1000 <= generate_pin() <= 9999 ) # ! pin is RANDOM
    def test_generate_default_start_time(self):
        self.assertEqual(generate_start_time() , Settings.load().default_start_time)
        

class SettingsModelTest(TestCase):
    def setUp(self):
        self.settings = Settings.load()

    def test_singleton(self):
        self.assertEqual(self.settings , Settings.load())

    def test_creation(self):
        self.assertEqual(self.settings.title, 'Drummerei')
        self.assertEqual(self.settings.subtitle, 'Open Decks Timetable')
        self.assertTrue(isinstance(self.settings, Settings))
        self.assertEqual(str(self.settings), self.settings.title)


class SlotModelTest(TestCase):
    def setUp(self):
        self.name = "TestDJ"
        self.start_time = datetime.now()

        self.slot = Slot.objects.create(
            name=self.name,
            start_time=self.start_time,
        )

    def test_creation(self):
        self.assertEqual(self.slot.name, self.name)
        self.assertEqual(self.slot.start_time, self.start_time)
        self.assertEqual(self.slot.slot_id, None)
        self.assertTrue(isinstance(self.slot, Slot))
        self.assertEqual(
            str(self.slot),
            f"None @ {self.slot.start_time}: {self.slot.name}"
        )

    def test_reserve(self):
        name = "TestDJ & TestMC"
        uuid = self.slot.reserve(name)
        self.assertNotEqual(uuid, None)
        self.assertEqual(self.slot.name, name)

    def test_clear_slot(self):
        self.slot.clear_slot()
        self.assertEqual(self.slot.name,None)
        self.assertEqual(self.slot.slot_id,None)

    def test_clear_slot_with_id(self):
        from uuid import uuid4
        name = "TestDJ & TestMC"
        uuid = self.slot.reserve(name)
        self.assertRaises(ValueError,self.slot.clear_slot_with_id,uuid4())
        self.assertEqual(self.slot.name,name)
        self.assertEqual(self.slot.slot_id,uuid)


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
            self.settings.url+"?pin="+str(self.schedule.pin)
        )

    def test_generate_qrcode(self):
        from PIL import Image
        from pyzbar import pyzbar

        img = Image.open(Settings.load().default_qr_code_path)
        output = pyzbar.decode(img)[0].data.decode("utf-8")
        self.assertEqual(output, self.schedule.generate_url_with_pin())
