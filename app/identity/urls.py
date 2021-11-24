from django.urls import path
from identity import views

app_name = 'identity'

urlpatterns = [
    path('register/', views.RegisterUserView.as_view(), name='register'),
    path('login/', views.LoginCreateTokenView.as_view(), name='login'),
    path('profile/', views.ManageUserView.as_view(), name='profile')
]
