from django.contrib.auth.views import LogoutView
from django.views.generic import TemplateView, DetailView

from core.models import Event


# Create your views here.
class LandingView(TemplateView):
    template_name = 'signup/index.html'


class SignupView(DetailView):
    template_name_field = 'template'
    model = Event
    queryset = Event.objects.filter(deleted=False)

class EventsLogoutView(LogoutView):
    template_name = 'signup/logout.html'
