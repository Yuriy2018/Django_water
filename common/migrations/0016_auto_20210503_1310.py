# Generated by Django 3.2 on 2021-05-03 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0015_alter_client_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='number_apart',
            field=models.CharField(blank=True, max_length=15, null=True, verbose_name='Номер кв.'),
        ),
        migrations.AlterField(
            model_name='client',
            name='number_home',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Номер дома'),
        ),
    ]
