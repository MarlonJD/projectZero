from django.urls import path
from . import views

app_name = 'label'

urlpatterns = [
    path('', views.indexLabelTemplateView.as_view(), name="index"),
]
