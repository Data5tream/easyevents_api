from django.urls import path

from . import views

urlpatterns = [
    path('profile', views.ProfileView.as_view(), name='profile'),
    path('dashboard', views.DashboardView.as_view(), name='dashboard'),
    path('events', views.EventList.as_view(), name='event_list'),
    path('event/new', views.EventDetails.as_view(), name='create_event'),
    path('event/<int:pk>', views.EventDetails.as_view(), name='event_details'),
    path('event/<int:pk>/participants', views.EventParticipants.as_view(), name='event_participants'),
    path('account/change_password', views.ChangePassword.as_view(), name='change_password'),
    path('account/details', views.ChangeAccountDetails.as_view(), name='change_details'),
]
