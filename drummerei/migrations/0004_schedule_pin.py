# Generated by Django 5.1.5 on 2025-01-19 23:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drummerei', '0003_alter_schedule_slots'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='pin',
            field=models.IntegerField(default=8298),
        ),
    ]
