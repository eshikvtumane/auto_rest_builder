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
