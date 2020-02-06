from django.urls import path
from . import views

app_name = 'label'

urlpatterns = [
    path('', views.indexLabelTemplateView.as_view(), name="index"),
    path('distribution/', views.distLabelListView.as_view(),
         name='distribution'),
    path('distribution/add/', views.addDistLabelView, name='addDist'),
    path('contentID/', views.contentIDLabelListView.as_view(),
         name='contentID'),
    path('contentID/request/', views.contentIDLabelRequestCreateView.as_view(),
         name='contentIDRequest'),
    path('statistic/', views.statisticLabelListView.as_view(),
         name='statistic'),
    path('statement/', views.statementLabelListView.as_view(),
         name='statement'),
]
