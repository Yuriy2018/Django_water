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

    class Meta:
        model = DeleviryDistricts
        fields = '__all__'


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
    class Meta:
        model = TabluarOrders
        fields = '__all__'


class OrdersListSerializer(serializers.ModelSerializer):
    tabulars = TabularOrdersListSerializer(many=True)

    class Meta:
        model = Order
        fields = '__all__'


class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class TabluarOrdersCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TabluarOrders
        fields = '__all__'
