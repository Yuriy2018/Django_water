# Generated by Django 3.2 on 2021-05-18 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0010_auto_20210518_1158'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='comment',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Комментарий'),
        ),
    ]
