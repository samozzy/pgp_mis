# Generated by Django 3.2.16 on 2022-10-28 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('programming', '0035_alter_show_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='year',
            field=models.IntegerField(help_text='The year the event is taking place. The latest year will be used as the default year for "current" lists.', null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='title',
            field=models.CharField(default='Edinburgh Fringe', help_text="What is the event? (Typically you won't change this)", max_length=250),
        ),
    ]
