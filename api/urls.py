from django.urls import path

from api.views import models_list, add_record, delete_record

urlpatterns = [
    path('', models_list, name="project_models_list"),
    path('<str:app_label_name>/<str:model_name>/add/', add_record, name="add_record"),
    path('<str:app_label_name>/<str:model_name>/delete/<int:pk>', delete_record, name="delete_record"),
]
