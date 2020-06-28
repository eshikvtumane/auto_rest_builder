from django.urls import path

from api.views import models_list, add_record

urlpatterns = [
    path('', models_list, name="project_models_list"),
    path('<str:app_label_name>/<str:model_name>/add/', add_record, name="add_record"),
]
