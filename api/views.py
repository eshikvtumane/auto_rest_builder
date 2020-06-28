from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse, HttpRequest

from api.auto_rest import AutoRest


def models_list(request: HttpRequest) -> JsonResponse:
    result = list(ContentType.objects.all().values("app_label", "model"))
    return JsonResponse(result, safe=False)


def get_records(request: HttpRequest, app_label_name: str, model_name: str) -> JsonResponse:
    auto_rest = AutoRest('GET', app_label_name, model_name, request)
    return auto_rest.get_result()


def add_record(request: HttpRequest, app_label_name: str, model_name: str) -> JsonResponse:
    auto_rest = AutoRest('POST', app_label_name, model_name, request)
    return auto_rest.get_result()


def delete_record(request: HttpRequest, app_label_name: str, model_name: str, pk: int) -> JsonResponse:
    auto_rest = AutoRest('DELETE', app_label_name, model_name, request, pk)
    return auto_rest.get_result()


def update_record(request: HttpRequest, app_label_name: str, model_name: str, pk: int) -> JsonResponse:
    auto_rest = AutoRest('PUT', app_label_name, model_name, request, pk)
    return auto_rest.get_result()


