from django.db import models


# Create your models here.
class Theme(models.Model):
    title = models.CharField("标题名称", max_length=64, default="Andon管理系统")
    theme_id = models.AutoField(primary_key=True)
    theme_color = models.CharField(
        "主题色", max_length=128, null=True, blank=True, default="#3dcd58"
    )
    aux_color = models.CharField(
        "辅色", max_length=128, null=True, blank=True, default="#696969"
    )
    corporate_logo = models.ImageField(
        "LOGO", max_length=300, null=True, upload_to="theme"
    )
    tab_logo = models.ImageField(
        "TAB_LOGO", max_length=300, null=True, upload_to="theme"
    )
    login_logo = models.ImageField(
        "LOGIN_LOGO", max_length=300, null=True, upload_to="theme"
    )

    def to_dict(self):
        return {
            "title": self.title,
            "corporate_logo": self.corporate_logo.url,
            "tab_logo": self.tab_logo.url,
            "login_logo": self.login_logo.url,
            "self_color": self.theme_color,
            "aux_color": self.aux_color,
        }
