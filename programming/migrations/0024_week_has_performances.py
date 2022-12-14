# Generated by Django 3.2.16 on 2022-10-20 23:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('programming', '0023_auto_20221020_1750'),
    ]

    operations = [
        migrations.AddField(
            model_name='week',
            name='has_performances',
            field=models.BooleanField(default=True, help_text='Whether there are performances on this week. Eg W0 and W4 will likely not.'),
        ),
    ]
