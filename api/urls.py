from rest_framework import routers
from django.urls import path, include
from . import views

router = routers.DefaultRouter()
router.register(r'genre', views.GenreViewSet, basename='genres')

urlpatterns = [
    path('', include(router.urls)),
    path('loadTracks/<aid>/', views.loadTracksAPIView.as_view()),
    path('loadPlatforms/<aid>/', views.loadPlatformsAPIView.as_view()),
    path('addGenre/', views.addGenre, name="addGenre"),
    path('removeGenre/',
         views.removeGenre,
         name="removeGenre"),
]
