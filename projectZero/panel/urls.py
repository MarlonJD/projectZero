from django.urls import path
from . import views

app_name = 'panel'

urlpatterns = [
    path('', views.indexView, name='index'),
    path('distribution', views.distView, name='distribution'),
    path('trackUpload', views.trackUpload, name='trackUpload'),
    path('addDist', views.adddistUserView, name='addDist'),
]
