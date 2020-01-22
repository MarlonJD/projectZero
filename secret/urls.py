from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'secret'

urlpatterns = [
    path('', views.indexAdminTemplateView.as_view(), name='index'),
    path('distribution/', views.distributionAdminListView.as_view(),
         name='distribution'),
    path('distribution/<pk>/', views.distributionAdminDetailView.as_view(),
         name='distribution-detail'),
    path('distribution/update/<pk>/', views.distributionAdminUpdateView.as_view(),
         name='distribution-update'),
    path('distribution/delete/<pk>/', views.distributionAdminDeleteView.as_view(),
         name='distribution-delete'),
    path('user/', views.userAdminListView.as_view(),
         name='user'),
    path('user/register/', views.userSignUpAdminCreateView.as_view(),
         name='user-register'),
]
