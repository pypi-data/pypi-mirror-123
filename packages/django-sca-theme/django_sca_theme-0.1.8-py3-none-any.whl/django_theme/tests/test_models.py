from .case import ThemeBaseCase
from .theme import ThemeCase


class EnglishThemeTest(ThemeBaseCase):
    def setUp(self) -> None:
        self.theme_case = ThemeCase()

    def test_english_name(self):
        """TODO: not finished yet. """
