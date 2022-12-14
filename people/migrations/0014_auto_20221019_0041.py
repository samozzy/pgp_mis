# Generated by Django 3.2.16 on 2022-10-18 23:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0013_auto_20221018_2350'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='pronouns',
            field=models.CharField(blank=True, help_text='eg "he / him", "she / her", "they / them"', max_length=50),
        ),
        migrations.AlterField(
            model_name='person',
            name='middle_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='Middle name(s)'),
        ),
    ]
