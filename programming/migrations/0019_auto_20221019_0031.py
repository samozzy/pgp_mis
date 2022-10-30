# Generated by Django 3.2.16 on 2022-10-18 23:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('programming', '0018_event_accepting_submissions'),
    ]

    operations = [
        migrations.AddField(
            model_name='show',
            name='copy_long',
            field=models.TextField(blank=True, help_text='Around 100 words'),
        ),
        migrations.AddField(
            model_name='show',
            name='copy_short',
            field=models.TextField(blank=True, help_text='Around 50 words'),
        ),
    ]
