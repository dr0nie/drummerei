from datetime import datetime, timedelta

from django.test import TestCase

from ..models.settings import Settings

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
