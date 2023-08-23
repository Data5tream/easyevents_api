from django.urls import path

from . import views

urlpatterns = [
    path('profile', views.ProfileView.as_view(), name='profile'),
    path('events', views.EventList.as_view(), name='event_list'),
    path('event/new', views.EventDetails.as_view(), name='create_event'),
    path('event/<int:pk>', views.EventDetails.as_view(), name='event_details')
]
