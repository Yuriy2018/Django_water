# Generated by Django 3.2 on 2021-08-26 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0028_alter_client_date_returned'),
    ]

    operations = [
        migrations.AddField(
            model_name='positions',
            name='min_count',
            field=models.IntegerField(default=0, verbose_name='минимальное количество'),
        ),
    ]
