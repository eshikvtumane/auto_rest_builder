import json
from django.apps import apps
from django.forms import model_to_dict
from django.http import JsonResponse, HttpRequest
from http import HTTPStatus
from typing import Dict, Any


class AutoRest:
    def __init__(self, wait_method:str, app_label_name:str, model_name:str, request: HttpRequest, pk: int = None):
        self._wait_method = wait_method
        self._app_label_name = app_label_name
        self._model_name = model_name
        self._pk = pk
        self._request = request

    def get_result(self) -> JsonResponse:
        if not self.__is_nessesary_http_method():
            return self.__create_error_response("Error! Wrong http method.", HTTPStatus.FORBIDDEN)

        try:
            model = self.__get_model()

            method_obj = self.__get_method_object_for_http_method()
            result = method_obj(model)
            response = self.__create_success_response(result)
            return response
        except Exception as e:
            # return self.__create_error_response("Error! Wrong app label or model name.")
            return self.__create_error_response("Error! {}.".format(str(e)))

    def __is_nessesary_http_method(self) -> bool:
        if self._wait_method.lower() == self._request.method.lower():
            return True
        return False

    def __get_model(self):
        return apps.get_model(self._app_label_name, self._model_name)

    def __create_error_response(self, message: str, http_status: HTTPStatus = HTTPStatus.INTERNAL_SERVER_ERROR) \
            -> JsonResponse:
        return JsonResponse(
            status=http_status,
            data={
                "error": message
            },
        )

    def __create_success_response(self, message: Any, http_status: HTTPStatus = HTTPStatus.OK) -> JsonResponse:
        return JsonResponse(
            status=http_status,
            data={
                "result": message,
            },
            safe=False,
        )

    def __get_method_object_for_http_method(self):
        method_name = '{}'.format(self._wait_method.lower())
        return getattr(self, method_name)

    def get(self, model) -> [Dict[Any, Any]]:
        params = self._request.GET.copy()
        limit = params.pop('limit', 100)
        order_by = params.pop('order_by', 'pk')
        columns_filter = params

        result = list(model.objects.filter(**columns_filter).order_by(order_by)[:limit].values())
        return result

    def post(self, model) -> Dict[Any, Any]:
        body = self.__get_request_body()
        created_obj = model.objects.create(**body)
        created_obj_json = model_to_dict(created_obj)
        return created_obj_json

    def delete(self, model) -> Dict[str, str]:
        model.objects.filter(pk=self.__pk).delete()
        return {"result": "Object has been delete success."}

    def put(self, model) -> Dict[Any, Any]:
        body = self.__get_request_body()

        updated_obj = model.objects.get(pk=self._pk)
        updated_obj.update(**body)
        updated_obj_json = model_to_dict(updated_obj.refresh_from_db())
        return updated_obj_json

    def __get_request_body(self) -> Dict[Any, Any]:
        body_unicode = self._request.body.decode('utf-8')
        body = json.loads(body_unicode)
        return body