# Generated by Django 3.2.16 on 2022-10-30 00:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('staffing', '0014_alter_application_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='application',
            options={'permissions': [('dir_can_offer_application', 'Can review and offer applications')], 'verbose_name': 'Volunteer Application', 'verbose_name_plural': 'Volunteer Applications'},
        ),
    ]
