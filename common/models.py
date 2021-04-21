from django.db import models

class Type_address(models.Model):
    name = models.CharField(max_length=50, verbose_name='Тип', unique=True)

    class Meta:
        verbose_name = 'Тип адреса'
        verbose_name_plural = 'Типы адресов'

    def __str__(self):
        return self.name

class Gardens(models.Model):
    name = models.CharField(max_length=50, verbose_name='Наименование', unique=True)

    class Meta:
        verbose_name = 'Садоводческий коллектив'
        verbose_name_plural = 'Садоводческие коллективы'

    def __str__(self):
        return self.name

class Driver(models.Model):
    name = models.CharField(max_length=50, verbose_name='Водитель', unique=True)

    class Meta:
        verbose_name = 'Водитель'
        verbose_name_plural = 'Водители'

    def __str__(self):
        return self.name

class DeleviryDistricts(models.Model):
    name = models.CharField(max_length=50, verbose_name='Район', unique=True)
    driver = models.ForeignKey(Driver, verbose_name='Водитель',on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Район доставки'
        verbose_name_plural = 'Районы доставки'

    def __str__(self):
        return self.name

class Streets(models.Model):
    name = models.CharField(max_length=50, verbose_name='Улица', unique=True)
    type = models.ForeignKey(Type_address,verbose_name='Тип', on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Улица'
        verbose_name_plural = 'Улицы'

    def __str__(self):
        return self.name

class Positions(models.Model):
    name = models.CharField(max_length=50, verbose_name='Наименование', unique=True)
    code1C = models.CharField(max_length=11, verbose_name='Код 1С')
    price = models.IntegerField(verbose_name='Цена', default=0)

    class Meta:
        verbose_name = 'Номенклатура'
        verbose_name_plural = 'Номенклатура'

    def __str__(self):
        return self.name


class Client(models.Model):
    name = models.CharField(max_length=50, verbose_name='Наименование', unique=True)
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    phone_number = models.CharField(max_length=15, verbose_name='Телефон', unique=True)
    address = models.CharField(max_length=100, verbose_name='Адрес')
    code1C = models.CharField(max_length=11, verbose_name='Код 1С')

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return self.name