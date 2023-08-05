from django_theme.tests.case import ThemeBaseCase


class ThemeTest(ThemeBaseCase):
    def test_without_theme(self):
        response = self.client.get(self.api_theme_url)
        self.assertEqual(response.status_code, 200)
