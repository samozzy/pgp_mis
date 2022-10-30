# Generated by Django 3.2.16 on 2022-10-18 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('programming', '0005_auto_20221018_1420'),
    ]

    operations = [
        migrations.AlterField(
            model_name='show',
            name='get_in_dur',
            field=models.DurationField(default=0, verbose_name='Get-in duration'),
        ),
        migrations.AlterField(
            model_name='show',
            name='get_out_dur',
            field=models.DurationField(default=0, verbose_name='Get-out duration'),
        ),
        migrations.AlterField(
            model_name='show',
            name='level',
            field=models.CharField(choices=[('PRO', 'Professional'), ('EME', 'Emerging Professional'), ('SEM', 'Semi-Professional'), ('AMA', 'Amateur')], default='PRO', help_text='How established is the company?', max_length=30),
        ),
        migrations.AlterField(
            model_name='show',
            name='notes_general',
            field=models.TextField(blank=True, verbose_name='Notes (general)'),
        ),
        migrations.AlterField(
            model_name='show',
            name='status',
            field=models.CharField(choices=[('APP', 'Applied'), ('COM', 'Complete')], default='APP', help_text='Application status', max_length=30),
        ),
    ]
