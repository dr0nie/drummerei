# Generated by Django 5.1.5 on 2025-01-20 01:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drummerei', '0007_remove_slot_available_alter_schedule_pin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='pin',
            field=models.IntegerField(default=5127),
        ),
    ]
