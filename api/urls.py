from rest_framework import routers
from django.urls import path, include
from . import views

router = routers.DefaultRouter()
# router.register(r'cagriKonulari', CagriKonusuViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('loadTracks/<aid>/', views.loadTracksAPIView.as_view()),
    path('loadPlatforms/<aid>/', views.loadPlatformsAPIView.as_view()),
]
