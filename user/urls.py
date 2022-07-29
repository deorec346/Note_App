from django.urls import path

from user import views

urlpatterns = [
    path('login', views.UserLogin.as_view(), name='login_api'),
    path('register', views.UserRegistration.as_view(), name='register_api'),
    path('validate/<str:token>', views.ValidateToken.as_view(), name='validate'),
]