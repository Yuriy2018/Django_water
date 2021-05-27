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
        return obj.date.strftime("%d.%m.%Y %H:%M:%S")

    date_wiev.admin_order_field = 'date'
    date_wiev.short_description = 'Дата документа'

    # list_display = ('id', 'time_seconds',)
    list_display = ('number', 'date_wiev', 'client', 'show_driver', 'amount', 'number1С', 'new_client', 'create_bot', 'user', 'load_1C')
    list_display_links = ('number', 'date_wiev', 'client',)
    inlines = [TabluarOrdersInline, ]
    fields = [('number', 'number1С'),'date', 'status_order','client', 'type_play', 'amount', 'comment', 'returned_container',('user', 'load_1C')]
    autocomplete_fields = ['client',]

    # change_form_template = ''

    def show_driver(self, obj):
        return obj.client.driver

    show_driver.short_description = "Водитель"


    def get_readonly_fields(self, request, obj=None):
        if obj:  # when editing an object
            return ['amount', 'number1С', 'number']
        return self.readonly_fields

class TabluarOrderAdmin(admin.ModelAdmin):
    # list_display = ('id', 'time_seconds',)
    list_display = ('id','order', 'position', 'price', 'quantity', 'amount')
    list_display_links = ('order', 'position', 'price', 'quantity', 'amount')

admin.site.register(Order, OrderAdmin)
# admin.site.register(TabluarOrders, TabluarOrderAdmin)
admin.site.site_header = 'Онлайн заказ воды'