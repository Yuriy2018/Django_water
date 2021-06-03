from django.db import models
from django.contrib.auth.models import User

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
from documents.models import Order


class Driver(models.Model):
    name = models.CharField(max_length=50, verbose_name='Водитель', unique=True)
    user = models.OneToOneField(User, verbose_name="Пользователь", on_delete=models.PROTECT, null=True, blank=True)
    email = models.CharField(max_length=50, verbose_name='Почта', null=True, blank=True)
    login = models.CharField(max_length=50, verbose_name='Логин', null=True, blank=True)
    password = models.CharField(max_length=50, verbose_name='Пароль', null=True, blank=True)
    plane = models.PositiveSmallIntegerField(verbose_name='План заявок в день', default=80, blank=True)

    class Meta:
        verbose_name = 'Водитель'
        verbose_name_plural = 'Водители'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):

        if self.email or (self.login and self.password):
            old = Driver.objects.filter(pk=self.pk).first()
            if old:
                if old.email != self.email or old.login != self.login or old.password != self.password:
                    if self.user:
                        self.user.email = self.email
                        self.user.username = self.login
                        self.user.last_name = self.login
                        self.user.set_password(self.password)
                        self.user.save()
                        # message = f'У Вас сменился логин или пароль:\nЛогин: {self.login}\nПароль: {self.password}'
                        # send_mail('Доступ к системе отчётов', message=message, from_email='ari@auto-door.kz',
                        #           recipient_list=[self.email])
            if not self.user:
                self.user = User.objects.create_user(username=self.login, password=self.password, email=self.email)
                # message = f'Доброго времени суток! Вам предоставлен доступ к системе отчётов, учёта и регистрации заявок компании "Imperial Group".\
                #         \n\nСсылка для входа: http://ari.auto-door.kz/' \
                #           f'\n\nЛогин: {self.login}\n\nПароль: {self.password}\n\n\nС уважением, ARI.'
                # send_mail('Доступ к системе отчётов', message=message, from_email='ari@auto-door.kz',
                #           recipient_list=[self.email])
        super().save(*args, **kwargs)

    def get_open_orders(self):
        return Order.objects.filter(client__driver=self).exclude(status_order= Order.STATUS_TYPE_COMPLETED)

class District(models.Model):
    name = models.CharField(max_length=50, verbose_name='Район', unique=True)

    class Meta:
        verbose_name = 'Район'
        verbose_name_plural = 'Районы'

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
        (PAY_TYPE_CASHLESS, 'Перечисление')
    )

    name = models.CharField(max_length=100, verbose_name='Наименование')
    district = models.ForeignKey(District, verbose_name='Район', on_delete=models.PROTECT, null=True, blank=True)
    street = models.CharField(max_length=50, verbose_name='Улица', blank=True, null=True)
    number_home = models.CharField(max_length=20, verbose_name='Номер дома', blank=True, null=True)
    number_apart = models.CharField(max_length=15, verbose_name='Номер кв.', blank=True, null=True)
    address = models.CharField(max_length=100, verbose_name='Адрес', blank=True, null=True)
    object_name = models.CharField(max_length=100, verbose_name='Название объекта', blank=True, null=True)
    phone_number = models.CharField(max_length=30, verbose_name='Телефон', null=True)
    driver = models.ForeignKey(Driver, verbose_name='Водитель', on_delete=models.PROTECT, null=True, blank=True)
    # first_name = models.CharField(max_length=50, verbose_name='Имя', blank=True, null=True)
    # last_name = models.CharField(max_length=50, verbose_name='Фамилия', blank=True, null=True)
    type_client = models.CharField(max_length=15, verbose_name='Тип клиента', default=CLIENT_TYPE_PERSON, null=True,
                                   choices=CLIENT_TYPE_CHOICES)
    type_play = models.CharField(max_length=15, verbose_name='Тип оплаты', default=PAY_TYPE_CASH, null=True,
                                 choices=PAY_TYPE_CHOICES)
    code1C = models.CharField(max_length=11, verbose_name='Код 1С', blank=True, null=True)
    comment = models.CharField(max_length=250, verbose_name='Комментарий', null=True, blank=True)



    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return self.address

    def save(self, *args, **kwargs):
        self.address = ' '.join([name for name in [self.district, self.street, self.number_home, self.number_apart] if name])
        if not self.address:
            self.address = self.name
        super().save(*args, **kwargs)