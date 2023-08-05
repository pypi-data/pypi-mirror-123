from django.core.files import File

from ..models import Theme


class ThemeCase:
    """
    create a sample theme
    """

    def __init__(self, corporate_logo_path="theme/theme/logo.jpg",
                 tab_logo_path="theme/theme/tab_logo.png",
                 login_logo_path="theme/theme/login_logo.jpg"):
        self.theme = {
            "title": "天和双利",
            "theme_color": "#e60000",
            "aux_color": "#666666",
        }
        self.theme_object = self.create_theme()

        self.theme_object.corporate_logo.save(
            "logo.jpg", File(open(corporate_logo_path, "rb"))
        )
        self.theme_object.tab_logo.save(
            "tab_logo.png", File(open(tab_logo_path, "rb"))
        )
        self.theme_object.login_logo.save(
            "login_logo.jpg", File(open(login_logo_path, "rb"))
        )

    def attach_file(self):
        return [
            (
                "corporate_logo",
                ("logo.jpg", open("theme/theme/logo.jpg", "rb"), "image/jpg"),
            ),
            (
                "tab_logo",
                (
                    "tab_logo.png",
                    open("theme/theme/tab_logo.png", "rb"),
                    "image/png"
                ),
            ),
            (
                "login_logo",
                (
                    "login_logo.jpg",
                    open("theme/theme/login_logo.jpg", "rb"),
                    "image/jpg"
                ),
            ),
        ]

    def create_theme(self):
        return Theme.objects.create(**self.theme)
