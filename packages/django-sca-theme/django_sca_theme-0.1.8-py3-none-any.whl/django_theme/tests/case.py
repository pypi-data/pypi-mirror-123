from django.test import TestCase


class ThemeBaseCase(TestCase):
    def setUp(self) -> None:
        self.api_theme_url = "/api/system/theme"
