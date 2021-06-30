from django.urls import path

from django.contrib import admin

from .views import user_login, report_view, order_driver_view, procces_order,report_view_today

urlpatterns = [
    # url(r'^$', views.index, name='index'),
    path('', user_login, name='user_login'),
    path('report/', report_view, name = 'report'),
    path('report_today/<str:period>', report_view_today, name = 'report_today'),
    path('admin/', admin.site.urls),
    path('order_driver/<int:id>/', order_driver_view, name='order_driver'),
    path('procces_order/', procces_order, name='procces_order'),

    # path('documents/order/add/', admin.site.urls),
    ]