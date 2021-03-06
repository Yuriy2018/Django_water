# Generated by Django 3.2 on 2021-07-14 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0026_auto_20210625_0027'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='date_returned',
            field=models.DateField(null=True, verbose_name='Дата возврата'),
        ),
        migrations.AddField(
            model_name='client',
            name='gone',
            field=models.BooleanField(blank=True, default=False, verbose_name='Ушёл'),
        ),
    ]
