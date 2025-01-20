from datetime import datetime, timedelta

from django.test import TestCase

from .models import Settings, Schedule, Slot

class SettingsModelTest(TestCase):
    def setUp(self):
        self.settings = Settings.load()

    def test_settings_creation(self):
        self.assertEqual(self.settings.title, 'Drummerei')
        self.assertEqual(self.settings.subtitle, 'Open Decks Timetable')
        self.assertTrue(isinstance(self.settings, Settings))
        self.assertEqual(str(self.settings), self.settings.title)

class ScheduleModelTest(TestCase):
    def setUp(self):
        self.start_time = datetime.now()
        self.end_time=self.start_time + timedelta(hours=4)

        self.schedule = Schedule(
            start_time=self.start_time,
            end_time=self.end_time,
        )

    def test_schedule_creation(self):
        self.assertEqual(self.schedule.start_time, self.start_time)
        self.assertEqual(self.schedule.end_time, self.end_time )
        self.assertTrue(isinstance(self.schedule, Schedule))

        self.assertTrue(1000 <= self.schedule.pin <= 9999 ) # ! pin is RANDOM
        self.assertEqual(str(self.schedule), str(self.schedule.start_time.date()))

class SlotModelTest(TestCase):
    def setUp(self):
        self.name = "TestDJ"
        self.time = datetime.now()

        self.slot = Slot(
            name=self.name,
            time=self.time,
        )

    def test_schedule_creation(self):
        self.assertEqual(self.slot.name, self.name)
        self.assertEqual(self.slot.time, self.time)
        self.assertTrue(isinstance(self.slot, Slot))
        self.assertEqual(str(self.slot), self.slot.name)
