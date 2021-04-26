from django.http import HttpResponse, JsonResponse

from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import PositionsListSerializer, DriversListSerializer, \
    ClientsListSerializer, GardensListSerializer, DeleviryDistrictsListSerializer, StreetsListSerializer, \
    OrdersListSerializer, TabularOrdersListSerializer, OrderCreateSerializer , TabluarOrdersCreateSerializer

from common.models import Client, Positions, Gardens, DeleviryDistricts, Streets
from documents.models import Order, TabluarOrders


class PositionListView(APIView):

    def get(self, request):
        positions = Positions.objects.all()
        serializer = PositionsListSerializer(positions, many=True)
        return Response(serializer.data)


class ClientView(APIView):

    def get(self, request, number):
        clients = Client.objects.filter(phone_number=number).first()
        serializer = ClientsListSerializer(clients)
        return Response(serializer.data)


class GardensView(APIView):

    def get(self, request):
        gardens = Gardens.objects.all()
        if not gardens:
            return Response([])

        serializer = GardensListSerializer(gardens, many=True)
        return Response(serializer.data)


class DistrictsView(APIView):

    def get(self, request):
        districts = DeleviryDistricts.objects.all()
        if not districts:
            return Response([])

        serializer = DeleviryDistrictsListSerializer(districts, many=True)
        return Response(serializer.data)


class StreetsView(APIView):

    def get(self, request):
        streets = Streets.objects.all()
        if not streets:
            return Response([])

        serializer = StreetsListSerializer(streets, many=True)
        return Response(serializer.data)


class OrderView(APIView):

    def get(self, request, number):
        orders = Order.objects.filter(client__phone_number=number).order_by('-date').first()
        if not orders:
            return Response([])

        serializer = OrdersListSerializer(orders)
        return Response(serializer.data)

    def post(self, request):
        order = OrdersListSerializer(data=request.data)
        if order.is_valid():
            order.save()
        return Response(status=201)


class OrderCreateView(APIView):

    def get(self, request):
        orders = Order.objects.all().first()
        if not orders:
            return Response([])

        serializer = OrdersListSerializer(orders)
        return Response(serializer.data)

    def post(self, request):
        order = OrderCreateSerializer(data=request.data)
        if order.is_valid():
            order.save()
            table = request.data.get('tabulars')
            id_order = order.data.get('id')
            for row in table:
                row['order'] = id_order
            tabluars = TabluarOrdersCreateSerializer(data=table, many=True)
            if tabluars.is_valid():
                tabluars.save()
                # order.save()
                # if bool(tabluars.data):
                # order = Order.objects.get(id=id_order)
                # if order:
                #     order.save()
        return Response(status=201)

class TabuluarCreateView(APIView):

    def get(self, request):
        orders = TabluarOrders.objects.first()
        if not orders:
            return Response([])

        serializer = TabluarOrdersCreateSerializer(orders)
        return Response(serializer.data)

    def post(self, request):
        tabluars = TabluarOrdersCreateSerializer(data=request.data, many=True)
        if tabluars.is_valid():
            tabluars.save()
            if bool(tabluars.data):
                id_order =  tabluars.data[0]['order']
                order = Order.objects.get(id=id_order)
                if order:
                    order.save()
        return Response(status=201, data=order.id)

# class OrdersListView(APIView):
#
#     def get(self, request, number):
#         orders = Order.objects.filter(client__phone_number=number).order_by('-date').first()
#         if not orders:
#             return Response([])
#
#         serializer = OrdersListSerializer(orders)
#         return Response(serializer.data)

class Orders1cListView(APIView):

    def get(self, request):
        orders = Order.objects.filter(number1С=None)
        if not orders:
            return Response([])

        serializer = OrdersListSerializer(orders, many=True)
        return Response(serializer.data)

class ClientCreateView(APIView):

    def post(self, request):
        client = ClientsListSerializer(data=request.data)
        if client.is_valid():
            client.save()
        return Response(status=201, data=client.data)


def index(request):
    return HttpResponse("Hello, World!")
