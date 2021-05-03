from django.contrib import admin
from .models import Order, TabluarOrders


class TabluarOrdersInline(admin.TabularInline):
    model = TabluarOrders
    verbose_name = 'строка табличная часть'
    verbose_name_plural = 'Табличная часть'
    extra = 0

class OrderAdmin(admin.ModelAdmin):

    def date_wiev(self, obj):
        return obj.date.strftime("%d.%m.%Y %H:%M:%S")

    date_wiev.admin_order_field = 'date'
    date_wiev.short_description = 'Дата документа'

    # list_display = ('id', 'time_seconds',)
    list_display = ('number', 'date_wiev', 'client', 'amount', 'number1С')
    list_display_links = ('number', 'date_wiev', 'client', 'amount', 'number1С')
    inlines = [TabluarOrdersInline, ]
    fields = [('number', 'number1С'),'date', 'client', 'amount']


    def get_readonly_fields(self, request, obj=None):
        if obj:  # when editing an object
            return ['amount', 'number1С', 'number']
        return self.readonly_fields

class TabluarOrderAdmin(admin.ModelAdmin):
    # list_display = ('id', 'time_seconds',)
    list_display = ('id','order', 'position', 'price', 'quantity', 'amount')
    list_display_links = ('order', 'position', 'price', 'quantity', 'amount')

admin.site.register(Order, OrderAdmin)
admin.site.register(TabluarOrders, TabluarOrderAdmin)
admin.site.site_header = 'Онлайн заказ воды'