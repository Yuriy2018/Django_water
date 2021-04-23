# Generated by Django 3.2 on 2021-04-18 05:51

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('common', '0004_client'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(blank=True, null=True, verbose_name='Номер')),
                ('date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата регистрации')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='common.client', verbose_name='Контрагент')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
            },
        ),
        migrations.CreateModel(
            name='TabluarOrders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField(default=0, verbose_name='Цена')),
                ('quantity', models.IntegerField(default=0, verbose_name='Количество')),
                ('amount', models.IntegerField(default=0, verbose_name='Сумма')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='documents.order', verbose_name='Ссылка')),
                ('position', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='common.positions', verbose_name='Номенклатура')),
            ],
            options={
                'verbose_name': 'Строка табличной части заказа',
                'verbose_name_plural': 'Строки табличной части заказа',
            },
        ),
    ]