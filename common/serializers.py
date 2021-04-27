from rest_framework import serializers

from .models import Client, DeleviryDistricts, Driver, Gardens, Streets, Positions
from documents.models import Order, TabluarOrders


class PositionsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Positions
        fields = '__all__'


class ClientsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'


class DeleviryDistrictsListSerializer(serializers.ModelSerializer):
    driver = serializers.SlugRelatedField(slug_field='name', read_only=True)
    driver_data = serializers.SerializerMethodField('get_driver_data')

    class Meta:
        model = DeleviryDistricts
        fields = '__all__'

    def get_driver_data(self, DeleviryDistricts):
        return {'name': DeleviryDistricts.driver.name,
                # 'code1C': DeleviryDistricts.driver.code1C,
                'id': DeleviryDistricts.driver.id, }


class DriversListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = '__all__'


class GardensListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gardens
        fields = '__all__'


class StreetsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Streets
        fields = '__all__'


class TabularOrdersListSerializer(serializers.ModelSerializer):
    position_data = serializers.SerializerMethodField('get_position_data')
    class Meta:
        model = TabluarOrders
        fields = '__all__'
        # fields = ('order', 'position', 'price', 'quantity', 'amount', 'position_data')

    def get_position_data(self,tabuluarorders):
        return {'name' : tabuluarorders.position.name,
                'code1C': tabuluarorders.position.code1C,
                'id': tabuluarorders.position.id,}



class OrdersListSerializer(serializers.ModelSerializer):
    tabulars = TabularOrdersListSerializer(many=True)

    class Meta:
        model = Order
        fields = '__all__'


class OrdersList1сSerializer(serializers.ModelSerializer):
    client_data = serializers.SerializerMethodField('get_client_data')
    tabulars = TabularOrdersListSerializer(many=True)

    class Meta:
        model = Order
        fields = '__all__'

    def get_client_data(self,order):
        return {'name' : order.client.name,
                'code1C': order.client.code1C,
                'phone_number': order.client.phone_number,
                'address': order.client.address,
                'id': order.client.id,}


class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class TabluarOrdersCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TabluarOrders
        fields = '__all__'

