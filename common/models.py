from django.db import models


# class Type_address(models.Model):
#     name = models.CharField(max_length=50, verbose_name='Тип', unique=True)
#
#     class Meta:
#         verbose_name = 'Тип адреса'
#         verbose_name_plural = 'Типы адресов'
#
#     def __str__(self):
#         return self.name


# class Gardens(models.Model):
#     name = models.CharField(max_length=50, verbose_name='Наименование', unique=True)
#
#     class Meta:
#         verbose_name = 'Садоводческий коллектив'
#         verbose_name_plural = 'Садоводческие коллективы'
#
#     def __str__(self):
#         return self.name


class Driver(models.Model):
    name = models.CharField(max_length=50, verbose_name='Водитель', unique=True)

    class Meta:
        verbose_name = 'Водитель'
        verbose_name_plural = 'Водители'

    def __str__(self):
        return self.name

class District(models.Model):
    name = models.CharField(max_length=50, verbose_name='Район', unique=True)

    class Meta:
        verbose_name = 'Район'
        verbose_name_plural = 'Районы'

    def __str__(self):
        return self.name

# class DeleviryDistricts(models.Model):
#     name = models.CharField(max_length=50, verbose_name='Район', unique=True)
#     driver = models.ForeignKey(Driver, verbose_name='Водитель', on_delete=models.PROTECT)
#
#     class Meta:
#         verbose_name = 'Район доставки'
#         verbose_name_plural = 'Районы доставки'
#
#     def __str__(self):
#         return self.name


# class Streets(models.Model):
#     name = models.CharField(max_length=50, verbose_name='Улица', unique=True)
#     type = models.ForeignKey(Type_address, verbose_name='Тип', on_delete=models.PROTECT)
#
#     class Meta:
#         verbose_name = 'Улица'
#         verbose_name_plural = 'Улицы'
#
#     def __str__(self):
#         return self.name


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
    CLIENT_TYPE_COMPANY = 'company'
    CLIENT_TYPE_PERSON = 'private_person'

    CLIENT_TYPE_CHOICES = (
        (CLIENT_TYPE_COMPANY, 'Компания'),
        (CLIENT_TYPE_PERSON, 'Частное лицо')
    )

    PAY_TYPE_CASH = 'cash'
    PAY_TYPE_CASHLESS = 'cashless'

    PAY_TYPE_CHOICES = (
        (PAY_TYPE_CASH, 'Наличный'),
        (PAY_TYPE_CASHLESS, 'Безналичный')
    )

    name = models.CharField(max_length=100, verbose_name='Наименование')
    district = models.ForeignKey(District, verbose_name='Район', on_delete=models.PROTECT, null=True, blank=True)
    street = models.CharField(max_length=50, verbose_name='Улица', blank=True, null=True)
    number_home = models.CharField(max_length=10, verbose_name='Номер дома', blank=True, null=True)
    number_apart = models.CharField(max_length=10, verbose_name='Номер кв.', blank=True, null=True)
    address = models.CharField(max_length=100, verbose_name='Адрес', blank=True, null=True)
    object_name = models.CharField(max_length=100, verbose_name='Название объекта', blank=True, null=True)
    phone_number = models.CharField(max_length=30, verbose_name='Телефон', null=True)
    driver = models.ForeignKey(Driver, verbose_name='Водитель', on_delete=models.PROTECT, null=True)
    # first_name = models.CharField(max_length=50, verbose_name='Имя', blank=True, null=True)
    # last_name = models.CharField(max_length=50, verbose_name='Фамилия', blank=True, null=True)
    type_client = models.CharField(max_length=15, verbose_name='Тип клиента', default=CLIENT_TYPE_PERSON, null=True,
                                   choices=CLIENT_TYPE_CHOICES)
    type_play = models.CharField(max_length=15, verbose_name='Тип оплаты', default=PAY_TYPE_CASH, null=True,
                                 choices=PAY_TYPE_CHOICES)
    code1C = models.CharField(max_length=11, verbose_name='Код 1С', blank=True, null=True)



    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.address = ' '.join([name for name in [self.district, self.street, self.number_home, self.number_apart] if name])