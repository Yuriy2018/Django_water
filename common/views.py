from django.http import HttpResponse, JsonResponse

from rest_framework.response import Response

from common.models import Client, Positions, District
from documents.models import Order, TabluarOrders



def index(request):
    return HttpResponse("Hello, World!")
