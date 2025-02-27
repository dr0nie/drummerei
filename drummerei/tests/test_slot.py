from datetime import datetime, timedelta

from django.test import TestCase

from ..models.settings import Settings
from ..models.slot import Slot, generate_start_time
from ..models.schedule import Schedule

class HelperFunctionsTest(TestCase):
    def test_generate_default_start_time(self):
        self.assertEqual(generate_start_time() , Settings.load().default_start_time)
        
class SlotModelTest(TestCase):
    def setUp(self):
        self.name = "TestDJ"
        self.start_time = datetime.now()

        self.slot = Slot.objects.create(
            name=self.name,
            start_time=self.start_time,
        )

        self.schedule = Schedule.objects.create(
            start_time=datetime.now()-timedelta(hours=1),
            end_time=datetime.now()+timedelta(hours=3),
            unlock_hours=1
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

    def test_is_reserved(self):
        slot = self.schedule.slots.first()
        self.assertFalse(slot.is_reserved())
        slot.reserve("DJ XY and Z")
        self.assertTrue(slot.is_reserved())

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

    def test_is_available(self):
        slot = self.schedule.slots.last()
        self.assertFalse(
            slot.is_available(),
            f"{slot} vs now: {datetime.now()}"
        )

        slot = self.schedule.slots.first()
        self.assertFalse(
            slot.is_available(),
            f"{slot} vs now: {datetime.now()}"
        )

        index_after_locked_hours = (self.schedule.unlock_hours*2)-1
        slot = list(self.schedule.slots.all())[index_after_locked_hours]
        self.assertFalse(
            slot.is_available(),
            f"{slot} vs now: {datetime.now()}"
        )

        index_in_time = 3#(self.schedule.unlock_hours*2)-1
        slot = list(self.schedule.slots.all())[index_in_time]
        self.assertTrue(
            slot.is_available(),
            f"{slot} vs now: {datetime.now()}"
        )
