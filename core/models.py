from datetime import datetime, timezone

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator
from django.db import models


def validate_datetime(timestamp):
    if timestamp < datetime.now():
        raise ValidationError("Date can't be in the past")


# Create your models here.
class User(AbstractUser):
    confirmed = models.BooleanField(default=False, blank=True)


class UserConfirmationCode(models.Model):
    code = models.CharField(max_length=64)
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="confirmation_codes")
    created = models.DateTimeField(auto_now_add=True)
    used = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return f"{self.user.email} ({'Used' if self.used else 'Not used'}): {self.code}"


class Event(models.Model):
    DEFAULT = 'signup/form_base.html'

    TEMPLATE_CHOICES = [
        (DEFAULT, 'Base'),
        ('signup/form_dark.html', 'Dark'),
        ('signup/form_mild.html', 'Mild'),
    ]

    creator = models.ForeignKey("User", on_delete=models.PROTECT, related_name="created_events")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=128)
    description = models.CharField(blank=True, null=True, max_length=512)
    participants = models.ManyToManyField("User", "joined_events", blank=True)
    max_participants = models.PositiveSmallIntegerField(default=8, validators=[
        MaxValueValidator(512, message="Events are currently limited to 512 participants max.")
    ])
    require_confirmation = models.BooleanField(default=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    signup_start = models.DateTimeField()
    signup_end = models.DateTimeField()
    deleted = models.BooleanField(default=False, blank=True)
    locked = models.BooleanField(default=False, blank=True)
    template = models.CharField(max_length=128, choices=TEMPLATE_CHOICES, default=DEFAULT)
    details_url = models.URLField(blank=True, null=True)

    @property
    def signup_is_open(self):
        return self.signup_start < datetime.now(timezone.utc) < self.signup_end

    @property
    def signup_not_open_yet(self):
        return self.signup_start > datetime.now(timezone.utc)

    @property
    def signup_closed_event_not_started(self):
        return self.signup_end < datetime.now(timezone.utc) < self.start_date

    @property
    def is_running(self):
        return self.start_date < datetime.now(timezone.utc) < self.end_date

    @property
    def is_over(self):
        return self.end_date < datetime.now(timezone.utc)

    @property
    def is_full(self):
        return self.max_participants <= self.participants.count()

    def available_seats(self):
        return self.max_participants - self.participants.count()

    def clean(self):
        super().clean()
        if self.start_date > self.end_date:
            raise ValidationError("End date must be after start date")
        if self.signup_start > self.signup_end:
            raise ValidationError("Signup end date must be after signup start date")
        if self.signup_end > self.start_date:
            raise ValidationError("Signup end date can't be after event start.")

    def __str__(self):
        return f"{self.pk} - \"{self.title}\" by {self.creator.username}"

    class Meta:
        ordering = ['-created']


class EventUpdate(models.Model):
    DEFAULT_TYPE = 'joined'
    EVENT_TYPES = [
        (DEFAULT_TYPE, 'Joined'),
        ('left', 'Left'),
        ('kicked', 'Kicked'),
    ]

    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="updates")
    event = models.ForeignKey("Event", on_delete=models.CASCADE, related_name="updates")
    event_type = models.CharField(max_length=16, choices=EVENT_TYPES, default=DEFAULT_TYPE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def clean(self):
        super().clean()
        if self.event.deleted or self.event.locked:
            raise ValidationError("Event not available")

    def __str__(self):
        return f"{self.pk} - {self.user.username} {self.event_type} {self.event.title} ({self.event.pk})"

    class Meta:
        ordering = ['-timestamp']
