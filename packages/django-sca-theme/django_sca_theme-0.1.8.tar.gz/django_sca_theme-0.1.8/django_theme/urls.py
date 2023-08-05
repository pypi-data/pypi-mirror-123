from django.urls import path

from .views import SystemStyleView

urlpatterns = [
    path("api/system/theme", SystemStyleView.as_view()),
]
