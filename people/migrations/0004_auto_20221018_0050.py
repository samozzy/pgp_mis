# Generated by Django 3.2.16 on 2022-10-17 23:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('programming', '0001_initial'),
        ('people', '0003_auto_20221018_0050'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='allergies',
            field=models.ManyToManyField(blank=True, to='people.Allergy'),
        ),
        migrations.AlterField(
            model_name='person',
            name='company',
            field=models.ManyToManyField(blank=True, to='programming.Company'),
        ),
    ]
