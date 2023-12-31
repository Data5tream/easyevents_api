# Generated by Django 4.2.4 on 2023-08-23 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_event_end_date_alter_event_max_participants_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='require_confirmation',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='description',
            field=models.CharField(blank=True, max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='end_date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='event',
            name='signup_end',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='event',
            name='signup_start',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='event',
            name='start_date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='event',
            name='title',
            field=models.CharField(max_length=128),
        ),
    ]
