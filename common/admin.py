from django.contrib import admin

from .models import Driver, Positions, Client, District

class ClientAdmin(admin.ModelAdmin):

    # list_display = ('id', 'time_seconds',)
    list_display = ('name', 'phone_number', 'driver','code1C')
    list_display_links = ('name', 'phone_number', 'driver','code1C')
    # fields = [('name', 'object_name'),
    #           ('district', 'street', 'number_home', 'number_apart'),
    #           ('address','phone_number'),
    #           ('type_client','type_play'),
    #           ('driver','code1C'),
    #           ]
    search_fields = ['name']

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



admin.site.register(Positions, PositionsAdmin)
admin.site.register(Driver)
admin.site.register(District, DistrictAdmin)
# admin.site.register(Gardens)
# admin.site.register(Streets)
# admin.site.register(DeleviryDistricts, DeleviryDistrictsAdmin)
# admin.site.register(Type_address)
admin.site.register(Client, ClientAdmin)

admin.site.site_header = 'Онлайн заказ воды'