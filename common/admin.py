from django.contrib import admin

from .models import Driver, Positions, Client, District

def make_published(modeladmin, request, queryset):
    for client in queryset:
        if not client.address:
            client.address = client.name
            client.save()
make_published.short_description = "Заполнить строку адрес"

class ClientAdmin(admin.ModelAdmin):


    # list_display = ('id', 'time_seconds',)
    list_display = ('name', 'phone_number', 'driver','comment','code1C')
    list_display_links = ('name', 'phone_number', 'driver','comment','code1C')
    actions = [make_published]
    # fields = [('name', 'object_name'),
    #           ('district', 'street', 'number_home', 'number_apart'),
    #           ('address','phone_number'),
    #           ('type_client','type_play'),
    #           ('driver','code1C'),
    #           ]
    search_fields = ['name', 'phone_number']

class DistrictAdmin(admin.ModelAdmin):
    class Meta:
        abstract = True
        ordering = ['name']

    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    # search_fields = ['name']


class PositionsAdmin(admin.ModelAdmin):
    list_display = ('name', 'price' , 'code1C')

# class DeleviryDistrictsAdmin(admin.ModelAdmin):
#     list_display = ('name', 'driver')
#     list_filter = ('driver',)

class DriverAdmin(admin.ModelAdmin):
    list_display = ('name', 'Open_Order', 'user', 'login', 'email')
    list_display_links = ('name', 'Open_Order', 'user', 'login', 'email')

    def Open_Order(self, obj):
        return len(obj.get_open_orders())

    Open_Order.short_description = 'Открытые ордера'




admin.site.register(Positions, PositionsAdmin)
admin.site.register(Driver, DriverAdmin)
admin.site.register(District, DistrictAdmin)
# admin.site.register(Gardens)
# admin.site.register(Streets)
# admin.site.register(DeleviryDistricts, DeleviryDistrictsAdmin)
# admin.site.register(Type_address)
admin.site.register(Client, ClientAdmin)

admin.site.site_header = 'Онлайн заказ воды'