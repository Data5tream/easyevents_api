from django.contrib import messages
from django.contrib.auth.views import LogoutView
from django.http import HttpResponse, Http404
from django.shortcuts import redirect
from django.views.generic import TemplateView, DetailView
from rest_framework import status

from core.models import Event, EventUpdate


# Create your views here.
class LandingView(TemplateView):
    template_name = 'signup/index.html'


class SignupView(DetailView):
    template_name_field = 'template'
    model = Event
    queryset = Event.objects.filter(deleted=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['already_joined'] = self.request.user in context['event'].participants.all()
        return context

    def post(self, request, pk, title):
        if not request.user.is_authenticated:
            return HttpResponse(status=status.HTTP_403_FORBIDDEN)

        try:
            event = Event.objects.get(pk=pk, deleted=False)
        except Event.DoesNotExist:
            raise Http404

        if event.creator == request.user:
            messages.add_message(request, messages.ERROR, 'Can\'t join an event you have created.')
        elif event.signup_is_open:
            if request.user not in event.participants.all():
                # Add user to event participants
                event.participants.add(request.user)
                event.save()

                # Create event update
                event_update = EventUpdate()
                event_update.user = request.user
                event_update.event = event
                event_update.type = 'joined'
                event_update.save()

                messages.add_message(request, messages.SUCCESS, 'Successfully joined event.')
            else:
                messages.add_message(request, messages.INFO, 'Already signed up for event.')

        return redirect('signup_view', pk=pk, title=title)


class EventsLogoutView(LogoutView):
    template_name = 'signup/logout.html'
