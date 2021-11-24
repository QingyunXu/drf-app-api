from django.urls import path, include
from rest_framework.routers import DefaultRouter

from song import views

app_name = 'song'

router = DefaultRouter()
router.register('playlist', views.PlayListViewSet)

urlpatterns = [
    path('', include(router.urls))
]
