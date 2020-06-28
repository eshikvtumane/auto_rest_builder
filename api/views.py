from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse


def models_list(request):
    result = list(ContentType.objects.all().values("app_label", "model"))
    return JsonResponse(result, safe=False)
