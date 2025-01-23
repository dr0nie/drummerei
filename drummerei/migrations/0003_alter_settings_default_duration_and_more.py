# Generated by Django 5.1.5 on 2025-01-23 13:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drummerei', '0002_settings_default_qr_code_path_alter_schedule_slots'),
    ]

    operations = [
        migrations.AlterField(
            model_name='settings',
            name='default_duration',
            field=models.DurationField(default=datetime.timedelta(seconds=14400), help_text='The default duration for schedules.'),
        ),
        migrations.AlterField(
            model_name='settings',
            name='default_qr_code_path',
            field=models.CharField(default='drummerei/static/image/qr.png', help_text='The default path for storing QR code images.', max_length=255),
        ),
        migrations.AlterField(
            model_name='settings',
            name='default_slot_duration',
            field=models.DurationField(default=datetime.timedelta(seconds=1800), help_text='The default duration for individual slots.'),
        ),
        migrations.AlterField(
            model_name='settings',
            name='default_start_time',
            field=models.TimeField(default=datetime.time(20, 0), help_text='The default start time for slots.'),
        ),
        migrations.AlterField(
            model_name='settings',
            name='subtitle',
            field=models.CharField(default='Open Decks Timetable', help_text='A subtitle for the application.', max_length=255),
        ),
        migrations.AlterField(
            model_name='settings',
            name='title',
            field=models.CharField(default='Drummerei', help_text='The title of the application.', max_length=255),
        ),
        migrations.AlterField(
            model_name='settings',
            name='url',
            field=models.CharField(blank=True, help_text='The URL associated with the application.', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='slot',
            name='name',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
