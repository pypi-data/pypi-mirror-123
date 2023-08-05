from django_theme.tests.case import ThemeBaseCase
from django_theme.libs.code import Code

from .theme import ThemeCase


class ThemeFunctionalTest(ThemeBaseCase):
    def setUp(self) -> None:
        ThemeCase()
        super().setUp()

    def assertResponse(self) -> dict:
        response = self.client.get(path=self.api_theme_url)
        self.assertEqual(response.status_code, 200)

        json_data = response.json()
        self.assertEqual(json_data.get("code"), Code.SUCCESS, msg=json_data.get("msg"))
        return json_data

    def test_get_theme_details(self):
        """
        获取系统配置：主题色，logo等：每个系统只会有一个配置所以获取第一个可以满足需求
        不鉴权
        """

        theme_data = self.assertResponse().get("data").get("title")
        self.assertEqual(theme_data, "天和双利")

    def test_get_theme_logo(self):
        json_data = self.assertResponse()
        tab_logo_path = json_data.get("data").get("tab_logo")
        self.assertTrue(
            tab_logo_path.startswith("/theme/theme"), msg=tab_logo_path
        )

    def test_get_login_logo(self):
        json_data = self.assertResponse()
        login_logo_path = json_data.get("data").get("login_logo")
        self.assertTrue(
            login_logo_path.startswith("/theme/theme"), msg=login_logo_path
        )
