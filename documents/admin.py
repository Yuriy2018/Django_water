from django.contrib import admin
from .models import Order, TabluarOrders


class TabluarOrdersInline(admin.TabularInline):
    model = TabluarOrders
    verbose_name = 'строка табличная часть'
    verbose_name_plural = 'Табличная часть'
    extra = 0


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
    date_dev_wiev.short_description = 'Дата клиента'

    def date_end_wiev(self, obj):
        if obj.date_end:
            return obj.date_end.strftime("%d.%m.%Y")

    date_end_wiev.admin_order_field = 'date_end'
    date_end_wiev.short_description = 'Дата закрытия'

    # list_display = ('id', 'time_seconds',)
    list_display = ('attention','number', 'date_wiev', 'client', 'comment','date_dev_wiev', 'date_end_wiev', 'show_driver', 'amount', 'number1С', 'create_bot')
    list_display_links = ('number', 'date_wiev', 'client',)
    inlines = [TabluarOrdersInline, ]
    # fields = [('number', 'date'),('date_dev', 'date_end'),('status_order', 'type_play'),'client',  'amount', 'comment', 'returned_container',('user', 'load_1C', 'number1С')]
    fields = [('date_dev', 'date_end'),('status_order', 'type_play'),'client', 'comment', 'returned_container',('user', 'attention', 'load_1C', 'number1С')]
    autocomplete_fields = ['client',]
    readonly_fields = ['date_end',]

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