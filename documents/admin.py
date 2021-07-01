from django.contrib import admin
from .models import Order, TabluarOrders

from datetime import datetime, timedelta, date

def make_completed(modeladmin, request, queryset):
    for order in queryset:
        order.status_order = Order.STATUS_TYPE_COMPLETED
        order.save()
make_completed.short_description = "Заполнить статус - доставлен"

def make_postponed(modeladmin, request, queryset):
    for order in queryset:
        order.status_order = Order.STATUS_TYPE_postponed
        order.save()
make_postponed.short_description = "Заполнить статус - отложен"

class TabluarOrdersInline(admin.TabularInline):
    model = TabluarOrders
    verbose_name = 'строка табличная часть'
    verbose_name_plural = 'Табличная часть'
    extra = 0

class DateDeliveriFilter(admin.SimpleListFilter):
    title = 'Дата доставки'
    parameter_name = 'delivery'

    def lookups(self, request, model_admin):
        return (
            ('yesterday', 'Вчера'),
            ('today', 'Сегодня'),
            ('tomorrow', 'Завтра'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'yesterday':
            return queryset.filter(date_dev=date.today() - timedelta(days=1))
        elif self.value() == 'today':
            return queryset.filter(date_dev=date.today())
        elif self.value() == 'tomorrow':
            return queryset.filter(date_dev=date.today() + timedelta(days=1))


class OrderAdmin(admin.ModelAdmin):

    change_form_template = 'admin.html'

    def date_wiev(self, obj):
        return obj.date.strftime("%d.%m.%Y")

    date_wiev.admin_order_field = 'date'
    date_wiev.short_description = 'Дата документа'

    def date_dev_wiev(self, obj):
        if obj.date_dev:
            return obj.date_dev.strftime("%d.%m.%Y")

    date_dev_wiev.admin_order_field = 'date_dev'
    date_dev_wiev.short_description = 'Дата доставки'

    def date_end_wiev(self, obj):
        if obj.date_end:
            return obj.date_end.strftime("%d.%m.%Y")

    date_end_wiev.admin_order_field = 'date_end'
    date_end_wiev.short_description = 'Дата закрытия'

    # list_display = ('id', 'time_seconds',)
    list_display = ('attention','new_client', 'number', 'date_wiev', 'client', 'comment','date_dev_wiev', 'date_end_wiev', 'show_driver', 'status_order', 'number1С', 'create_bot')
    list_display_links = ('number', 'date_wiev', 'client',)
    inlines = [TabluarOrdersInline, ]
    # fields = [('number', 'date'),('date_dev', 'date_end'),('status_order', 'type_play'),'client',  'amount', 'comment', 'returned_container',('user', 'load_1C', 'number1С')]
    fields = [('date_dev', 'date_end'),('status_order', 'type_play'),'client', 'comment', 'returned_container',('user', 'attention', 'load_1C', 'number1С')]
    autocomplete_fields = ['client',]
    readonly_fields = ['date_end',]
    list_filter = ['new_client','status_order', 'client__driver']
    # list_filter = ('DateDeliveriFilter',)
    actions = [make_completed, make_postponed,]
    # change_form_template = ''

    def show_driver(self, obj):
        return obj.client.driver

    show_driver.short_description = "Водитель"


    def get_readonly_fields(self, request, obj=None):
        if obj:  # when editing an object
            return ['amount', 'number1С', 'number', 'date_end']
        return self.readonly_fields

class TabluarOrderAdmin(admin.ModelAdmin):
    # list_display = ('id', 'time_seconds',)
    list_display = ('id','order', 'position', 'price', 'quantity', 'amount')
    list_display_links = ('order', 'position', 'price', 'quantity', 'amount')

admin.site.register(Order, OrderAdmin)
# admin.site.register(TabluarOrders, TabluarOrderAdmin)
admin.site.site_header = 'Онлайн заказ воды'