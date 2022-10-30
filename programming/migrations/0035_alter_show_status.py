# Generated by Django 3.2.16 on 2022-10-28 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('programming', '0034_alter_show_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='show',
            name='status',
            field=models.CharField(choices=[('DRA', 'Draft'), ('APP', 'Applictation Submitted'), ('COM', 'Complete')], default='DRA', help_text='Application status', max_length=30),
        ),
    ]
