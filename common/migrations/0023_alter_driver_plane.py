# Generated by Django 3.2 on 2021-05-26 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0022_driver_plane'),
    ]

    operations = [
        migrations.AlterField(
            model_name='driver',
            name='plane',
            field=models.PositiveSmallIntegerField(blank=True, default=80, verbose_name='План заявок в день'),
        ),
    ]
