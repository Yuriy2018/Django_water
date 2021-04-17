from django.contrib import admin

from .models import Driver, Gardens, Streets, DeleviryDistricts, Type_address, Positions



class PositionsAdmin(admin.ModelAdmin):
    list_display = ('name', 'price' , 'code1C')

class DeleviryDistrictsAdmin(admin.ModelAdmin):
    list_display = ('name', 'driver')

admin.site.register(Positions, PositionsAdmin)
admin.site.register(Driver)
admin.site.register(Gardens)
admin.site.register(Streets)
admin.site.register(DeleviryDistricts, DeleviryDistrictsAdmin)
admin.site.register(Type_address)