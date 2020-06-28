from django.urls import path

from api.views import models_list, add_record, delete_record, update_record, get_records

urlpatterns = [
    path('', models_list, name="project_models_list"),
    path('<str:app_label_name>/<str:model_name>/get/', get_records, name="add_record"),
    path('<str:app_label_name>/<str:model_name>/add/', add_record, name="add_record"),
    path('<str:app_label_name>/<str:model_name>/delete/<int:pk>', delete_record, name="delete_record"),
    path('<str:app_label_name>/<str:model_name>/update/<int:pk>', update_record, name="update_record"),
]
