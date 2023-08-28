# Generated by Django 4.2.4 on 2023-08-28 10:30

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_event_template'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventupdate',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]