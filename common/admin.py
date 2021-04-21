from django.contrib import admin

from .models import Driver, Gardens, Streets, DeleviryDistricts, Type_address, Positions, Client



class PositionsAdmin(admin.ModelAdmin):
    list_display = ('name', 'price' , 'code1C')

class DeleviryDistrictsAdmin(admin.ModelAdmin):
    list_display = ('name', 'driver')
    list_filter = ('driver',)

admin.site.register(Positions, PositionsAdmin)
admin.site.register(Driver)
admin.site.register(Gardens)
admin.site.register(Streets)
admin.site.register(DeleviryDistricts, DeleviryDistrictsAdmin)
admin.site.register(Type_address)
admin.site.register(Client)

admin.site.site_header = 'Онлайн заказ воды'