# Generated by Django 3.2 on 2021-06-04 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0019_auto_20210603_2029'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateField(verbose_name='Дата от'),
        ),
    ]