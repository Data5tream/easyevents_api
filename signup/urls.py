from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.LandingView.as_view(), name='index'),
    path('login', auth_views.LoginView.as_view(template_name='signup/login.html'), name='login'),
    path('logout', auth_views.LogoutView.as_view(template_name='signup/logout.html'), name='logout'),
    path('signup/<int:pk>/<str:title>', views.SignupView.as_view(), name='signup_view'),
]
