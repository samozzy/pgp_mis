# Generated by Django 3.2.16 on 2022-10-21 00:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('programming', '0026_auto_20221021_0102'),
    ]

    operations = [
        migrations.AlterField(
            model_name='slot',
            name='has_preview',
            field=models.BooleanField(default=False, verbose_name='Add a preview performance'),
        ),
    ]
