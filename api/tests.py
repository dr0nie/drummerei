from datetime import datetime, timedelta
import json
from django.test import TestCase
from ninja.testing import TestClient

from drummerei.models.schedule import Schedule
from api.views.slots import router


class ApiTest(TestCase):
    def setUp(self):
        self.name = "TestDJ"
        self.start_time = datetime.now()
        self.end_time=self.start_time + timedelta(hours=4)

        self.schedule = Schedule.objects.create(
            start_time=self.start_time,
            end_time=self.end_time
        )
        self.client = TestClient(router)


    def test_reserve(self):
        response = self.client.patch(
            '1/slots/1/reserve',
            data=json.dumps({
                "name": "TestDJ",
                "pin": self.schedule.pin,
                }),
            content_type='application/json'
        )

        self.assertEqual(self.schedule.slots.first().name, self.name)
        self.assertEqual(response.json()["name"], self.name)

 
    def test_clear(self):
        response = self.client.patch(
            '1/slots/1/clear',
            data=json.dumps({
                "pin": self.schedule.pin,
                }),
            content_type='application/json'
        )

        self.assertEqual(self.schedule.slots.first().name, None)
        self.assertEqual(response.json()["name"], None)
