from django.urls import path
from . import views

app_name = 'secret'

urlpatterns = [
    path('', views.indexAdminTemplateView.as_view(), name='index'),
    path('distribution/', views.distributionAdminListView.as_view(),
         name='distribution'),
    path('distribution/<pk>/', views.distributionAdminDetailView.as_view(),
         name='distribution-detail'),
]
