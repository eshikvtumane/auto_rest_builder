from django.urls import path

from api.views import models_list

urlpatterns = [
    path('', models_list, name="project_models_list"),
]
