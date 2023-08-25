from django.contrib import admin
from django.forms import widgets, ModelForm

from .models import User, Event, EventUpdate


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


admin.site.register(User)
admin.site.register(EventUpdate)
