from django.urls import path, reverse
from . import views

app_name = 'panel'

urlpatterns = [
    path('', views.indexUserTemplateView.as_view(), name='index'),
    path('distribution/', views.distUserListView.as_view(),
         name='distribution'),
    path('distribution/add/', views.addDistUserView, name='addDist'),
    path('trackUpload/', views.trackUploadUser, name='trackUpload'),
    path('contentID/', views.contentIDUserListView.as_view(),
         name='contentID'),
    path('contentID/request/', views.contentIDUserRequestCreateView.as_view(),
         name='contentIDRequest'),
    path('statistic/', views.statisticUserListView.as_view(),
         name='statistic')
]
