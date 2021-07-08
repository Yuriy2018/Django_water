from django.urls import path

from django.contrib import admin

from .views import user_login, report_view, order_driver_view, procces_order,report_view_today, report_view_today_bs, report_view_today_bs_api

urlpatterns = [
    # url(r'^$', views.index, name='index'),
    path('', user_login, name='user_login'),
    path('report/', report_view, name = 'report'),
    # path('report/', report_view, name = 'report'),
    path('report_today/', report_view_today, name = 'report_today'),
    path('report_today_bs/', report_view_today_bs, name = 'report_today_bs'),
    path('report_today_bs_api/', report_view_today_bs_api, name = 'report_today_bs_api'),
    path('admin/', admin.site.urls),
    path('order_driver/<int:id>/', order_driver_view, name='order_driver'),
    path('procces_order/', procces_order, name='procces_order'),

    # path('documents/order/add/', admin.site.urls),
    ]