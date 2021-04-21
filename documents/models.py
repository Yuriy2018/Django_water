from django.db import models
from django.utils import timezone

from django.db.models import Sum

class Order(models.Model):
    number = models.IntegerField(verbose_name='Номер', null=True, blank=True)
    number1С = models.CharField(max_length=11, verbose_name='Номер 1С', null=True, blank=True)
    date = models.DateTimeField(verbose_name='Дата от', default=timezone.now)
    client = models.ForeignKey('common.Client',verbose_name='Контрагент', on_delete=models.PROTECT)
    amount = models.IntegerField(verbose_name='Сумма', default=0)


    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Заказ №{self.number} от {self.date.strftime("%d.%m.%Y %H:%M:%S")}'

    def save(self, *args, **kwargs):
        if not self.number:
            self.number = self.get_next_number()
        self.amount = self.get_amount()
        super().save(*args, **kwargs)

    def get_next_number(self):
        order = Order.objects.filter(number__isnull=False).values('number').order_by('-number').first()
        if order:
            return order['number'] + 1
        return 1

    def get_amount(self):
        return sum(TabluarOrders.objects.filter(order=self).values_list('amount', flat=True))


class TabluarOrders(models.Model):
    order = models.ForeignKey(Order,verbose_name='Ссылка', on_delete=models.PROTECT)
    position = models.ForeignKey('common.Positions',verbose_name='Номенклатура', on_delete=models.PROTECT)
    price =  models.IntegerField(verbose_name='Цена', default=0)
    quantity =  models.IntegerField(verbose_name='Количество', default=0)
    amount =  models.IntegerField(verbose_name='Сумма', default=0)


    class Meta:
        verbose_name = 'Строка табличной части заказа'
        verbose_name_plural = 'Строки табличной части заказа'

    # def __str__(self):
    #     return f'{self.number} от {self.date}'