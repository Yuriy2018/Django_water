from django.urls import path

from django.contrib import admin

from common.views import user_login, report_view

urlpatterns = [
    # url(r'^$', views.index, name='index'),
    path('', user_login, name='user_login'),
    path('report/', report_view),
    path('admin/', admin.site.urls),

    # path('documents/order/add/', admin.site.urls),
    ]