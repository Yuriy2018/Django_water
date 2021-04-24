from django.urls import path

from . import views

urlpatterns = [
    path('positions/', views.PositionListView.as_view()),
    path('gardens/', views.GardensView.as_view()),
    path('districts/', views.DistrictsView.as_view()),
    path('streets/', views.StreetsView.as_view()),
    path('get_last_order/<str:number>', views.OrderView.as_view()),
    path('get_client/<str:number>/', views.ClientView.as_view()),
    path('add_client/', views.ClientCreateView.as_view()),
    path('add_order/', views.OrderCreateView.as_view()),
    path('add_tabluars/', views.TabuluarCreateView.as_view()),
    ]