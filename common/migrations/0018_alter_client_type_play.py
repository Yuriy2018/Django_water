# Generated by Django 3.2 on 2021-05-18 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0017_alter_client_driver'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='type_play',
            field=models.CharField(choices=[('cash', 'Наличный'), ('cashless', 'Перечисление')], default='cash', max_length=15, null=True, verbose_name='Тип оплаты'),
        ),
    ]
