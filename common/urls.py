from django.urls import path

from django.contrib import admin

app_name = 'riddles'

urlpatterns = [
    # url(r'^$', views.index, name='index'),
    path('', admin.site.urls),
    ]