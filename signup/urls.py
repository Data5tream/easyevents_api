from django.urls import path

from . import views

urlpatterns = [
    path('', views.LandingView.as_view(), name='index'),
    path('signup/<int:pk>/<str:title>', views.SignupView.as_view(), name='signup_view'),
]
