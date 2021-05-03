from django.http import HttpResponse, JsonResponse

from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import PositionsListSerializer, DriversListSerializer, \
    ClientsListSerializer, \
    OrdersListSerializer, TabularOrdersListSerializer, OrderCreateSerializer, TabluarOrdersCreateSerializer, \
    OrdersList1сSerializer, DistrictListSerializer, ClientCreateSerializer

from common.models import Client, Positions, District
from documents.models import Order, TabluarOrders


class PositionListView(APIView):

    def get(self, request):
        positions = Positions.objects.all()
        serializer = PositionsListSerializer(positions, many=True)
        return Response(serializer.data)


class ClientView(APIView):

    def get(self, request, number):
        clients = Client.objects.filter(phone_number=number).first()
        if clients:
            serializer = ClientsListSerializer(clients)
            return Response(serializer.data)
        # else:
        #     return Response([])




class DistrictsView(APIView):

    def get(self, request):
        districts = District.objects.all()
        if not districts:
            return Response([])

        serializer = DistrictListSerializer(districts, many=True)
        return Response(serializer.data)


# class StreetsView(APIView):
#
#     def get(self, request):
#         streets = Streets.objects.all()
#         if not streets:
#             return Response([])
#
#         serializer = StreetsListSerializer(streets, many=True)
#         return Response(serializer.data)


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

        serializer = OrdersList1сSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        for value in request.data:
            Order.objects.filter(id=value['order_id']).update(number1С=value['number1C'])
        return Response(status=201,data='success')
            # ord = Order.objects.filter(id=value['order_id']).get()


class ClientCreateView(APIView):

    def post(self, request):
        client = ClientCreateSerializer(data=request.data)
        if client.is_valid():
            client.save()
        return Response(status=201, data=client.data)

