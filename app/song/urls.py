from django.urls import path, include
from rest_framework.routers import DefaultRouter

from song import views

app_name = 'song'

router = DefaultRouter()
router.register('playlist', views.PlayListViewSet)
router.register('singer', views.SingerViewSet)

urlpatterns = [
    path('', include(router.urls))
]
