from secrets import token_urlsafe

from django import forms
from django.contrib import messages
from django.core.mail import send_mail
from django.db import IntegrityError
from django.http import HttpResponse, Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import TemplateView, DetailView
from rest_framework import status

from core.models import Event, EventUpdate, User, UserConfirmationCode


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
        if not request.user.is_authenticated or not request.user.can_interact:
            return HttpResponse(status=status.HTTP_403_FORBIDDEN)

        try:
            event = Event.objects.get(pk=pk, deleted=False)
        except Event.DoesNotExist:
            raise Http404

        if request.POST.get('action') == 'join':
            if event.creator == request.user:
                messages.add_message(request, messages.ERROR, 'Can\'t join an event you have created.')
            elif event.is_full:
                messages.add_message(request, messages.ERROR, 'Event is full.')
            elif event.signup_is_open:
                if request.user not in event.participants.all():
                    # Add user to event participants
                    event.participants.add(request.user)
                    event.save()

                    # Create event update
                    event_update = EventUpdate()
                    event_update.user = request.user
                    event_update.event = event
                    event_update.event_type = 'joined'
                    event_update.save()

                    # Send event signup mail
                    send_mail(
                        f'Joined event {event.title} on Easy Events',
                        'TEST',
                        'test@localhost',
                        [request.user.email],
                        fail_silently=False,
                        html_message=''
                    )

                    messages.add_message(request, messages.SUCCESS, 'Successfully joined event.')
                else:
                    messages.add_message(request, messages.INFO, 'Already signed up for event.')
        elif request.POST.get('action') == 'leave':
            if event.signup_is_open:
                if request.user in event.participants.all():
                    # Remove user from event participants
                    event.participants.remove(request.user)
                    event.save()

                    # Create event update
                    event_update = EventUpdate()
                    event_update.user = request.user
                    event_update.event = event
                    event_update.event_type = 'left'
                    event_update.save()

                    # Send event signup mail
                    send_mail(
                        f'Left event {event.title} on Easy Events',
                        'TEST',
                        'test@localhost',
                        [request.user.email],
                        fail_silently=False,
                    )

                    messages.add_message(request, messages.SUCCESS, 'Successfully left event.')
            else:
                messages.add_message(request, messages.ERROR,
                                     'Can\'t leave the event, because the signup has finished.')

        return redirect('signup_view', pk=pk, title=title)


class RegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=64)
    last_name = forms.CharField(max_length=64)
    email = forms.EmailField()
    password0 = forms.CharField(min_length=8)
    password1 = forms.CharField(min_length=8)


class RegisterView(TemplateView):
    template_name = 'signup/register.html'

    def post(self, request):
        form = RegistrationForm(request.POST)
        next_url = request.POST['next'] if 'next' in request.POST else ''

        if form.is_valid():

            if form.cleaned_data['password0'] != form.cleaned_data['password1']:
                messages.add_message(request, messages.ERROR, 'Passwords don\'t match')
                return render(request, self.template_name, {'next': next_url})
            try:
                user = User.objects.create_user(
                    username=form.cleaned_data['email'],
                    email=form.cleaned_data['email'],
                    password=form.cleaned_data['password0'],
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'],
                )
            except IntegrityError:
                messages.add_message(request, messages.ERROR, 'Email already registered')
                return render(request, self.template_name, {'next': next_url})

            code = UserConfirmationCode(user=user, code=token_urlsafe(32))
            code.save()

            signup_link = f"{reverse('confirm_register')}?code={code.code}&next={next_url}"

            send_mail(
                'Easy Events Account Registration',
                f'To activate your Easy Events account open the following link:\n{signup_link}\n\nIf you haven\'t signed up for Easy Events you can safely ignore this email.',
                'noreply@easyevents.io',
                [user.email]
            )

            return render(request, 'signup/register_require_confirm.html')

        return render(request, self.template_name, {'form': form, 'next': next_url})


class ConfirmRegister(TemplateView):
    template_name = 'signup/register_confirmation.html'

    def get(self, request):
        if request.GET.get('code'):
            try:
                code = UserConfirmationCode.objects.get(code=request.GET.get('code'), used=False)
            except UserConfirmationCode.DoesNotExist:
                return render(request, self.template_name, {'error': 'invalid_code'})

            code.user.confirmed = True
            code.user.save()

            code.used = True
            code.save()

            next_url = request.GET.get('next') if request.GET.contains('next') else reverse('login')

            return render(request, self.template_name, {'next': next_url})

        return render(request, 'signup/register_confirmation.html', {'error': 'invalid_code'})
