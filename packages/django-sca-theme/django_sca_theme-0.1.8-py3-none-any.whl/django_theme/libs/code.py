# coding: utf-8

from enum import IntEnum
from typing import Any, Dict

from django.http import JsonResponse


class Code(IntEnum):
    ERROR = 0
    SUCCESS = 1
    FAILED = 2
    ACCESS_EXPIRED = 3
    REFRESH_EXPIRED = 4


def error_dict(msg: str) -> dict:
    return {"code": Code.FAILED.value, "msg": msg, "data": {}}


def error_response(msg: str) -> JsonResponse:
    return JsonResponse(data=error_dict(msg))


def success_dict(msg: str, data: dict) -> dict:
    return {"code": Code.SUCCESS, "msg": msg, "data": data}


def success_response(msg: str, data: dict) -> JsonResponse:
    return JsonResponse(data=success_dict(msg, data))


def error_data(data: Any) -> Dict:
    return {"code": Code.FAILED, "msg": "error", "data": data}


class ResponseMixin:
    def success_dict(self, msg, data):
        return success_dict(msg, data)

    def error_dict(self, msg):
        return error_dict(msg)
