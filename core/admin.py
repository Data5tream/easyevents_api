from django.contrib import admin
from django.forms import widgets, ModelForm

from .models import User, Event, EventUpdate, UserConfirmationCode


class EventAdminForm(ModelForm):
    class Meta:
        model = Event
        fields = '__all__'
        widgets = {
            'description': widgets.Textarea
        }


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    form = EventAdminForm
    filter_horizontal = ('participants',)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    filter_horizontal = ('groups', 'user_permissions')


admin.site.register(EventUpdate)
admin.site.register(UserConfirmationCode)
