from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from collections import Counter
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import PositionsListSerializer, DriversListSerializer, \
    ClientsListSerializer, \
    OrdersListSerializer, TabularOrdersListSerializer, OrderCreateSerializer, TabluarOrdersCreateSerializer, \
    OrdersList1сSerializer, DistrictListSerializer, ClientCreateSerializer, AuthSerialization, Client_add_fix_Serialization

from django.views.decorators.csrf import csrf_exempt
from common.models import Client, Positions, District, Driver
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



class ClientFullData(APIView):
    def get(self, request, number):
        list_num = []
        if len(number) > 10:
            list_num.append('7'+number[1:11])
            list_num.append('8'+number[1:11])
        else:
            list_num.append(number)
        client = Client.objects.filter(phone_number__in=list_num).first()
        if not client:
            return Response(status=201,data={"client_id" :"None",})

        driver = client.driver
        if driver:
            open_orders = list(driver.get_open_orders())
            open_ord = [str(x['date_dev']) for x in open_orders]
            c = Counter(open_ord)
            dict_open_ord = dict(c)

            driver_name = driver.name
            driver_plane = driver.plane
        else:
            open_orders = 0
            driver_name = ''
            driver_plane = 0

        orders = Order.objects.filter(client=client).order_by('-date').first()
        last_order = {}
        if orders:
            serializer = OrdersListSerializer(orders)
            last_order = serializer.data

        data = {'driver': driver_name,
                'plane': driver_plane,
                'open_orders': dict_open_ord,
                'client_id': client.id,
                'client_address': client.address,
                'client_name': client.name,
                'client_code1C': client.code1C,
                'last_order': last_order,
                }
        # return JsonResponse({'data': data})
        return Response(status=201, data=data)


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

class Autorization(APIView):

    def post(self, request):
        data = AuthSerialization(data=request.data)
        data_auth = data.initial_data
        login = data_auth['login']
        password = data_auth['password']
        driver = Driver.objects.filter(login=login,password=password).first()
        if driver:
            return Response(data={"id_driver":driver.id},status=200)
        else:
            return Response(data={"id_driver":"none"},status=200)



        # if order.is_valid():
        #     order.save()
        print('api/procces_order')
        return Response(status=200)

class OrdersForDriver(APIView):

    def get(self, request, id):
        driver = Driver.objects.filter(id=id)
        if not driver:
            return Response({"info":"Driver not fount"},status=200)

        orders = Order.objects.filter(Q(client__driver=driver[0]) & ~Q(status_order= Order.STATUS_TYPE_COMPLETED)).order_by('-date')
        if not orders:
            return Response({"info":"Orders not fount"},status=200)

        # serializer = OrdersListSerializer(orders,many=True)
        serializer = OrdersList1сSerializer(orders,many=True)
        return Response(serializer.data)

    # def post(self, request):
    #     order = OrdersListSerializer(data=request.data)
    #     if order.is_valid():
    #         order.save()
    #     return Response(status=201)

class ProccesOrder(APIView):

    def post(self, request):
        # order = OrdersListSerializer(data=request.data)
        # if order.is_valid():
        #     order.save()
        print('api/procces_order')
        return Response(status=201)


class Get_driver_order(APIView):

    # def get(self, request, name):
    #     data = Client_name_Serialization(data=request.data)
    #     client = Client.objects.filter(name=name)
    #     if client:
    #         client = client.first()
    #         driver = client.driver
    #         open_orders =  len(driver.get_open_orders())
    #         data = {'driver': driver,
    #                 'open_orders': open_orders,
    #                 }
    #         return JsonResponse({'data': data})
    #     # if order.is_valid():
    #     #     order.save()
    #     print('api/Get_driver_order')
    #     return Response(status=201)
    def post(self, request):
        if len(request.POST):
            client = Client.objects.get(pk=request.POST['id'])
        else:
            client = Client.objects.get(pk=request.data['id'])
        # if client:
        # client = client.first()
        driver = client.driver
        open_orders = len(driver.get_open_orders())

        if open_orders == 0:
            text = driver.name + ' ' + "нет активных ордеров"
        elif open_orders == 1:
            text = driver.name + ' ' + str(open_orders) + " активный ордер"
        elif open_orders == 2:
            text = driver.name + ' ' + str(open_orders) + " активных ордера"
        else:
            text = driver.name + ' ' + str(open_orders) + " активных ордеров"

        data = {'driver': driver.name,
                'plane': driver.plane,
                'open_orders': open_orders,
                'text': text,
                }
        return JsonResponse({'data': data})

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
        orders = Order.objects.filter(Q(number1С=None) & Q(load_1C=True))
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


class Add_client(APIView):

    def post(self, request):
        data = Client_add_fix_Serialization(data=request.data)
        for value in request.data:
            name = value['name'].lstrip()
            code1C = str(value['code'])
            if len(code1C) == 4:
                code = '00000' + code1C
            elif len(code1C) == 3:
                code = '000000' + code1C
            else:
                code = code1C
            type = value['type']
            type_client = Client.CLIENT_TYPE_COMPANY if type == 'Юр. лицо' else Client.CLIENT_TYPE_PERSON
            client = Client.objects.filter(name=name).first()
            if client:
                client.code1C = code
                client.save()
            else:
                newClient = Client.objects.create(name=name, code1C=code, address=name,type_client=type_client)
                newClient.save()
        return Response(status=201,data='success')
            # ord = Order.objects.filter(id=value['order_id']).get()