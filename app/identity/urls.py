from django.urls import path
from identity import views

app_name = 'identity'

urlpatterns = [
    path('register/', views.RegisterUserView.as_view(), name='register'),
    path('token/', views.CreateTokenView.as_view(), name='token')
]
