from django.contrib import admin

from .models import Theme


# Register your models here.


@admin.register(Theme)
class ThemeAdmin(admin.ModelAdmin):
    list_display = ("title", "theme_color", "aux_color")
