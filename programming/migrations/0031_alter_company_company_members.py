# Generated by Django 3.2.16 on 2022-10-21 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0016_auto_20221021_0145'),
        ('programming', '0030_company_company_members'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='company_members',
            field=models.ManyToManyField(blank=True, limit_choices_to={'person_type': 'COMPY'}, related_name='company_members', to='people.Person'),
        ),
    ]
