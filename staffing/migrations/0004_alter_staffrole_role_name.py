# Generated by Django 3.2.16 on 2022-10-18 23:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staffing', '0003_auto_20221019_0051'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staffrole',
            name='role_name',
            field=models.CharField(blank=True, help_text='A role offered on the staff, eg. Technician', max_length=100, unique=True),
        ),
    ]
