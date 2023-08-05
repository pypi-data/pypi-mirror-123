# Create your views here.
from typing import TYPE_CHECKING
from rest_framework.response import Response
from rest_framework.views import APIView

from django_theme.libs.code import error_dict, success_dict

from .models import Theme


class SystemStyleView(APIView):
    def get(self, request):
        style = Theme.objects.first()
        if not style:
            return Response(error_dict(msg="Theme config has not be set."))
        theme_dict = style.to_dict()
        return Response(success_dict(msg="success", data=theme_dict))
