from django.urls import path
from . import views

app_name = 'secret'

urlpatterns = [
    path('', views.indexAdminTemplateView.as_view(), name='index'),
    path('distribution/', views.distributionAdminListView.as_view(),
         name='distribution'),
    path('distribution/<pk>/', views.distributionAdminDetailView.as_view(),
         name='distribution-detail'),
    path('distribution/update/<pk>/',
         views.distributionAdminUpdateView.as_view(),
         name='distribution-update'),
    path('distribution/delete/<pk>/',
         views.distributionAdminDeleteView.as_view(),
         name='distribution-delete'),
    path('user/', views.userAdminListView.as_view(),
         name='user'),
    path('user/register/', views.userSignUpAdminCreateView.as_view(),
         name='user-register'),
    path('contentid/', views.contentIDAdminListView.as_view(),
         name='contentID'),
    path('contentid/update/<pk>/',
         views.contentIDAdminUpdateView.as_view(),
         name='contentID-update'),
    path('contentid/delete/<pk>/', views.contentIDAdminDeleteView.as_view(),
         name='contentID-delete'),
    path('statistic/', views.statisticAdminListView.as_view(),
         name='statistic'),
    path('statistic/add/', views.statisticAdminAddFunctionView,
         name='statistic-add'),
    path('statement/', views.statementsAdminListView.as_view(),
         name='statement'),
    path('statement/add/', views.statementAdminCreateView.as_view(),
         name='statement-add'),
    path('statement/update/<pk>/',
         views.statementAdminUpdateView.as_view(),
         name='statement-update'),
    path('statement/delete/<pk>/', views.statementAdminDeleteView.as_view(),
         name='statement-delete'),
    path('genre/', views.genreAdminListView.as_view(),
         name='genre'),
    path('genre/add/', views.genreAdminCreateView.as_view(),
         name='addGenre'),
]
