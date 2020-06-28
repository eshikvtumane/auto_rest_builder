import json

from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from django.forms import model_to_dict
from django.http import JsonResponse


def models_list(request) -> JsonResponse:
    result = list(ContentType.objects.all().values("app_label", "model"))
    return JsonResponse(result, safe=False)


def add_record(request, app_label_name: str, model_name: str) -> JsonResponse:
    if request.method == "POST":
        model = apps.get_model(app_label_name, model_name)

        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        created_obj = model.objects.create(**body)
        created_obj_json = model_to_dict(created_obj)
        return JsonResponse(created_obj_json)


def delete_record(request, app_label_name: str, model_name: str, pk: int) -> JsonResponse:
    if request.method == "DELETE":
        model = apps.get_model(app_label_name, model_name)

        model.objects.filter(pk=pk).delete()
        return JsonResponse({"result": "Object has been delete success."})


def update_record(request, app_label_name: str, model_name: str, pk: int) -> JsonResponse:
    if request.method == "PUT":
        model = apps.get_model(app_label_name, model_name)

        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        updated_obj = model.objects.get(pk=pk)
        updated_obj.update(**body)
        updated_obj_json = model_to_dict(updated_obj.refresh_from_db())
        return JsonResponse(updated_obj_json)
