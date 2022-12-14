# Generated by Django 3.2.16 on 2022-10-18 23:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('programming', '0016_alter_slot_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='slot',
            name='slot_status',
            field=models.CharField(choices=[('REQ', 'Requested'), ('OFF', 'Offered'), ('ACC', 'Accepted'), ('REJ', 'Rejected')], default='REQ', max_length=20),
        ),
    ]
