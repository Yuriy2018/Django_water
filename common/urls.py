from django.urls import path

from django.contrib import admin


urlpatterns = [
    # url(r'^$', views.index, name='index'),
    path('', admin.site.urls),
    # path('documents/order/add/', admin.site.urls),
    ]