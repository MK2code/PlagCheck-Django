from django.test import TestCase
from django.conf import settings

class SettingsTest(TestCase):
    def test_tesseract_cmd_is_configured(self):
        self.assertTrue(isinstance(settings.TESSERACT_CMD, str))
        self.assertTrue(len(settings.TESSERACT_CMD) > 0)
