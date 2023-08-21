from django.urls import path

from . import views

urlpatterns = [
    path('profile', views.ProfileView.as_view(), name='profile'),
    path('events', views.EventList.as_view(), name='event_list')
]
