from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Order(models.Model):

    PAY_TYPE_CASH = 'cash'
    PAY_TYPE_CASHLESS = 'cashless'

    PAY_TYPE_CHOICES = (
        (PAY_TYPE_CASH, 'Наличный'),
        (PAY_TYPE_CASHLESS, 'Перечисление')
    )

    STATUS_TYPE_NEW = 'new'
    STATUS_TYPE_COMPLETED = 'completed'
    STATUS_TYPE_postponed = 'postponed'

    STATUS_TYPE_CHOICES = (
        (STATUS_TYPE_NEW, 'Новый'),
        (STATUS_TYPE_COMPLETED, 'Завершен'),
        (STATUS_TYPE_postponed, 'Отложен')
    )

    number = models.IntegerField(verbose_name='Номер', null=True, blank=True)
    number1С = models.CharField(max_length=11, verbose_name='Номер 1С', null=True, blank=True)
    date = models.DateTimeField(verbose_name='Дата от', default=timezone.now)
    date_dev = models.DateField(verbose_name='Дата клиента', null=True)
    date_end = models.DateField(verbose_name='Дата закрытия', null=True, blank=True)
    client = models.ForeignKey('common.Client',verbose_name='Контрагент', on_delete=models.PROTECT)
    amount = models.IntegerField(verbose_name='Сумма', default=0)
    type_play = models.CharField(max_length=15, verbose_name='Тип оплаты', default=PAY_TYPE_CASH, null=True,
                                 choices=PAY_TYPE_CHOICES)
    status_order = models.CharField(max_length=15, verbose_name='Статус заказа', default=STATUS_TYPE_NEW, null=True,
                                 choices=STATUS_TYPE_CHOICES)

    comment = models.CharField(max_length=250, verbose_name='Комментарий', null=True, blank=True)
    returned_container = models.CharField(max_length=3, verbose_name='Возвращено бутылей', default=0, blank=True)
    new_client = models.BooleanField(verbose_name='Новый клиент', default=False, blank=True)
    create_bot = models.BooleanField(verbose_name='Чат-бот', default=False, blank=True)
    load_1C = models.BooleanField(verbose_name='Грузить в 1С', default=True, blank=True)
    user = models.OneToOneField(User, verbose_name="Пользователь", on_delete=models.PROTECT, null=True, blank=True)


    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        # return f'Заказ №{self.number} от {self.date.strftime("%d.%m.%Y %H:%M:%S")}'
        return f'Заказ №{self.number} от {self.date.strftime("%d.%m.%Y")}'

    def save(self, *args, **kwargs):
        if not self.number:
            self.number = self.get_next_number()
        if not self.date_dev:
            self.date_dev = self.date
        super().save(*args, **kwargs)
        # self.amount = self.get_amount()
        # super().save(*args, **kwargs)

    def get_next_number(self):
        order = Order.objects.filter(number__isnull=False).values('number').order_by('-number').first()
        if order:
            return order['number'] + 1
        return 1

    def get_amount(self):
        return sum(TabluarOrders.objects.filter(order=self).values_list('amount', flat=True))


class TabluarOrders(models.Model):
    order = models.ForeignKey(Order,verbose_name='Ссылка', on_delete=models.CASCADE, related_name='tabulars')
    position = models.ForeignKey('common.Positions',verbose_name='Номенклатура', on_delete=models.PROTECT, related_name='position_name')
    price =  models.IntegerField(verbose_name='Цена', default=0)
    quantity =  models.IntegerField(verbose_name='Количество', default=0)
    amount =  models.IntegerField(verbose_name='Сумма', default=0)


    class Meta:
        verbose_name = 'Строка табличной части заказа'
        verbose_name_plural = 'Строки табличной части заказа'

    # def __str__(self):
    #     return f'{self.number} от {self.date}'