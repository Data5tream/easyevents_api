from datetime import datetime, timezone

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


def validate_datetime(timestamp):
    if timestamp < datetime.now():
        raise ValidationError("Date can't be in the past")


# Create your models here.
class User(AbstractUser):
    pass


class Event(models.Model):
    creator = models.ForeignKey("User", on_delete=models.PROTECT, related_name="created_events")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=256)
    description = models.TextField(blank=True, null=True)
    participants = models.ManyToManyField("User", "joined_events", blank=True)
    max_participants = models.PositiveSmallIntegerField(default=8, validators=[
        MaxValueValidator(512, message="Events are currently limited to 512 participants max.")
    ])
    start_date = models.DateTimeField(validators=[MinValueValidator(datetime.now(timezone.utc).astimezone)])
    end_date = models.DateTimeField(validators=[MinValueValidator(datetime.now(timezone.utc).astimezone)])
    signup_start = models.DateTimeField(validators=[MinValueValidator(datetime.now(timezone.utc).astimezone)])
    signup_end = models.DateTimeField(validators=[MinValueValidator(datetime.now(timezone.utc).astimezone)])
    deleted = models.BooleanField(default=False, blank=True)
    locked = models.BooleanField(default=False, blank=True)

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


class EventUpdate(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="updates")
    event = models.ForeignKey("Event", on_delete=models.CASCADE, related_name="updates")
    type = models.CharField(max_length=16)

    def clean(self):
        super().clean()
        if self.event.deleted or self.event.locked:
            raise ValidationError("Event not available")
        if self.type not in ["joined", "left"]:
            raise ValidationError("Invalid update type.")

    def __str__(self):
        return f"{self.pk} - {self.user.username} {self.type} {self.event.title} ({self.event.pk})"
