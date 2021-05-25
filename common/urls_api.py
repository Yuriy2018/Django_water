from django.urls import path

from . import view_api as  views

urlpatterns = [

    # path('get_driver_client/<str:name>', views.get_driver),
    path('positions/', views.PositionListView.as_view()),
    # path('gardens/', views.GardensView.as_view()),
    # path('get_driver_client/', views.Get_driver_order.as_view()),
    path('get_driver_client/', views.get_driver),
    path('districts/', views.DistrictsView.as_view()),
    # path('get_driver/', views.Orders1cListView.as_view()),
    path('get_last_order/<str:number>', views.OrderView.as_view()),
    path('get_orders1c/', views.Orders1cListView.as_view()),
    path('get_client/<str:number>/', views.ClientView.as_view()),
    path('orders_for_driver/<int:id>/', views.OrdersForDriver.as_view()),
    path('add_client/', views.ClientCreateView.as_view()),
    path('procces_order/', views.ProccesOrder.as_view()),
    path('authorization/', views.Autorization.as_view()),
    # path('add_tabluars/', views.TabuluarCreateView.as_view()),
    ]