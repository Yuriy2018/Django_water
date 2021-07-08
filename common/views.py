from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from rest_framework.response import Response

import locale

from django.db.models import F, QuerySet

from documents.forms import OrderForm

import datetime
from datetime import date
from datetime import datetime, timedelta
from datetime import time

from common.forms import LoginForm
from common.models import Client, Positions, Driver
from documents.models import Order, TabluarOrders

from django.db.models import Q

locale.setlocale(locale.LC_ALL,'')

def index(request):
    return HttpResponse("Hello, World!")


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    if user.is_superuser:
                        login(request, user)
                        return redirect('/admin/')
                    else:
                        login(request, user)
                        return report_view(request)
                else:
                    # messages.error(request, 'Учетная запись не активна!')
                    return render(request, 'login.html', {'form': LoginForm()})
            else:
                # messages.error(request, 'Неверный логин или пароль!')
                return render(request, 'login.html', {'form': LoginForm()})
    else:
        # if request.user.is_superuser:
        #     login(request, request.user)
        #     return redirect('/admin/')

        if request.user.is_authenticated:
        #     return report_view(request)
        # else:
            return render(request, 'login.html', {'form': LoginForm()})

    return render(request, 'login.html', {'form': LoginForm()})



@login_required()
def report_view(request):
    if request.user:
        driver = Driver.objects.filter(user=request.user).first()
        if driver:
            orders = get_data_for_report(driver)
            data = {'driver': driver,
                    'orders' : orders}
            return render (request,'report_for_driver.html', data)
            # return HttpResponse("Тут должна быть информация для водителей!")
        else:
            return redirect('/admin/')
    # send_email_task()
    # dates = []
    # contact_person = ContactPerson.objects.get(user=request.user)
    # customer = contact_person.get_customer()
    # task = Task.objects.filter(branch__customer=customer).order_by('register_date').first()
    # if task:
    #
    #     date1 = task.register_date.date().replace(day=1)
    #     if date1 < timezone.now().date().replace(day=1):
    #         date2 = timezone.now().date().replace(day=1)
    #         while date1 < date2:
    #             dates.append(date1)
    #             date1 = date1 + relativedelta(months=1)
    #
    # contact_person = ContactPerson.objects.get(user=request.user)
    # # customer = Customer.objects.get(user=request.user)
    # customer = contact_person.get_customer()
    # cities = customer.get_cities()
    # branches = customer.get_branches()
    # return render(request, 'report.html',
    #               context={'random': random, 'branchs': branches, 'dates': dates, 'cities': cities})

def get_data_for_report(driver):
    # orders = Order.objects.filter(Q(client__driver=driver) | ~Q(status_order= Order.STATUS_TYPE_COMPLETED))
    # orders = Order.objects.filter(client__driver=driver).exclude(status_order= Order.STATUS_TYPE_COMPLETED)
    orders = driver.get_open_orders_full()
    data = []

    for inx, order in enumerate(orders):
        if order.date_dev != datetime.date.today():
            continue
        f = {'date':order.date,
         'client': order.client,
         'phone_number': order.client.phone_number,
         'type_pay': order.get_type_play_display(),
         'order': order,
         'order_id': order.id,
         'ref': "/order_driver/" + str(order.id) + '/',
         'number': order.number,
         'index': inx,
         'id_checkbox': 'id_checkbox_' + str(inx),
         'id_button': 'id_button_' + str(inx)
         }
        data.append(f)
    return data

# @login_required()
def report_view_today(request):

    if request.GET.get('period'):
        period = request.GET.get('period')
    else:
        period = '1'
    if period == '1':
        start = datetime.combine(date.today() - timedelta(days=1), time(17, 30, 00)) # Вчера вечер
        finish = datetime.combine(date.today(), time(8, 30, 00)) # сегодня утро
        period_str = '17:30 - 8:30'
    elif period == '2':
        start = datetime.combine(date.today(), time(8, 30, 00)) # Сегодня утро
        finish = datetime.combine(date.today(), time(17, 30, 00)) # Сегодня вечер
        period_str = '8:30 - 17:30'

    drivers = Driver.objects.all()
    data_dr = {}
    for driver in drivers:
        orders = driver.get_open_orders_detalis(start, finish)
        if not orders:
            continue
        data = []

        for inx, row in enumerate(orders):
            # if order.date_dev != datetime.date.today():
            #     continue
            f = {'num': inx + 1,
                 'date_dev': row.order.date_dev,
                 'district': row.order.client.district,
                 'address': row.order.client,
                 'phone_number': row.order.client.phone_number,
                 'position': row.position,
                 'quantity': row.quantity,
                 'amount': row.amount,
                 'comment': row.order.comment if row.order.comment != None else '' ,
                 'period_str': period_str ,
                 }
            data.append(f)
        # key = driver.name +' '+ datetime.date.today().strftime('%d.%m')
        key = driver.name
        data_dr[key] = data

    # Теперь для незаполненных водителей
    orders = TabluarOrders.objects.filter(order__client__driver=None,  order__date__gte=start, order__date__lte=finish).order_by('order__client__district')
    # orders = TabluarOrders.objects.filter(order__client__driver=None).order_by('order__client__district')
    if not orders:
        return render(request,'report_today.html',{'data' : data_dr})
    data = []

    for inx, row in enumerate(orders):
        # if order.date_dev != datetime.date.today():
        #     continue
        f = {'num': inx + 1,
             'date_dev': row.order.date_dev,
             'district': row.order.client.district,
             'address': row.order.client,
             'phone_number': row.order.client.phone_number,
             'position': row.position,
             'quantity': row.quantity,
             'amount': row.amount,
             'comment': row.order.comment if row.order.comment != None else '',
             'period_str': period_str,
             }
        data.append(f)
    # key = driver.name +' '+ datetime.date.today().strftime('%d.%m')
    key = "Не установлен"
    data_dr[key] = data
    return render(request,'report_today.html',{'data' : data_dr})

def report_view_today_bs(request):

    if request.GET.get('period'):
        period = request.GET.get('period')
    else:
        period = '1'
    if period == '1':
        start = datetime.combine(date.today() - timedelta(days=1), time(17, 30, 00))  # Вчера вечер
        finish = datetime.combine(date.today(), time(8, 30, 00))  # сегодня утро
        period_str = '17:30 - 8:30'
    elif period == '2':
        start = datetime.combine(date.today(), time(8, 30, 00))  # Сегодня утро
        finish = datetime.combine(date.today(), time(17, 30, 00))  # Сегодня вечер
        period_str = '8:30 - 17:30'
    # data = TabluarOrders.objects.filter(order__date__gte=start,
    #                                     order__date__lte=finish).order_by('order__client__district')
    data = TabluarOrders.objects.values(date_dev=F('order__date_dev'),
                                        driver=F('order__client__driver__name'),
                                        district=F('order__client__district__name'),
                                        address=F('order__client__name'),
                                        phone_number=F('order__client__phone_number'),
                                        position_=F('position__name'),
                                        quantity_=F('quantity'),
                                        amount_=F('amount'),
                                        comment=F('order__comment')
                                        )#.filter(order__date__gte=start,
                                        #order__date__lte=finish).order_by('driver')

    for val in data:
        # val['date_dev'] = str(val['date_dev'])
        if not val['district']:
            val['district'] = "Не установлен"

        if not val['driver']:
            val['driver'] = "Не установлен"

    return render(request, 'report_today_bs.html', {'data' : data, 'param': period})

def report_view_today_bs_api(request):

    if request.GET.get('period'):
        period = request.GET.get('period')
    else:
        period = '1'
    if period == '1':
        start = datetime.combine(date.today() - timedelta(days=1), time(17, 30, 00))  # Вчера вечер
        finish = datetime.combine(date.today(), time(8, 30, 00))  # сегодня утро
        period_str = '17:30 - 8:30'
    elif period == '2':
        start = datetime.combine(date.today(), time(8, 30, 00))  # Сегодня утро
        finish = datetime.combine(date.today(), time(17, 30, 00))  # Сегодня вечер
        period_str = '8:30 - 17:30'
    # data = TabluarOrders.objects.filter(order__date__gte=start,
    #                                     order__date__lte=finish).order_by('order__client__district')
    data = TabluarOrders.objects.values(date_dev=F('order__date_dev'),
                                        driver=F('order__client__driver__name'),
                                        district=F('order__client__district__name'),
                                        address=F('order__client__name'),
                                        phone_number=F('order__client__phone_number'),
                                        position_=F('position__name'),
                                        quantity_=F('quantity'),
                                        amount_=F('amount'),
                                        comment=F('order__comment')
                                        )#.filter(order__date__gte=start,
                                        #order__date__lte=finish).order_by('driver')
    dict_tabls = {}
    for val in data:
        val['date_dev'] = val['date_dev'].strftime('%d %B %Y')
        if not val['district']:
            val['district'] = "Не установлен"

        if not val['driver']:
            val['driver'] = "Не установлен"

        if dict_tabls.get(val['driver']):
            dict_tabls[val['driver']].append(val)
        else:
            dict_tabls[val['driver']] = []
            dict_tabls[val['driver']].append(val)

    columns = ['№','Дата доставки','Район','Адрес','Телефон','Номенклатура','Кол-во','Сумма','Коммент']

    str_thead = '<thead><tr>'
    for col in columns:
        str_thead += f'<th scope="col">{col}</th>'
    str_thead += '</tr></thead>'

    thead = '''<thead>
        <tr>
      <th scope="col">№</th>
      <th scope="col">Дата доставки</th>
      <th scope="col">Район</th>
      <th scope="col">Адрес</th>
      <th scope="col">Телефон</th>
      <th scope="col">Номенклатура</th>
      <th scope="col">Кол-во</th>
      <th scope="col">Сумма</th>
      <th scope="col">Коммент</th>
    </tr>
  </thead>'''

    list_tabls = []
    for table in dict_tabls:
        str_tbody = '<tbody>'
        cx = 0
        for values in dict_tabls[table]:
            str_tbody += '<tr>'
            cx += 1
            for ex, val in enumerate(values):
                if val == 'driver':
                    continue
                if ex == 0: # Если колонка первая строки, то добавляем еще нумерацию строки
                    str_tbody += f'<td scope="col">{str(cx)}</td>'
                str_tbody += f'<td scope="col">{str(values[val])}</td>'
    
            str_tbody += '</tr>'
        str_tbody += '</tbody>'
        list_tabls.append({'driver':table, 'str_tbody': str_tbody})

    # return render(request, 'report_today_bs.html', {'data' : data, 'driver' : Driver.objects.values_list('name').all()})
    return JsonResponse({'thead': str_thead, 'list_tabls': list_tabls})

def order_driver_view(request, id):
    order = Order.objects.filter(pk=id).first()
    form = OrderForm(instance=order)

    tabulars = TabluarOrders.objects.filter(order_id=id)
    tab_ls = []
    cx = 0
    for row in tabulars:
        cx += 1
        tab_ls.append({'position' : row.position,
                       'number' : str(cx),
                       'price' : row.price,
                       'position_id' : row.position.id,
                       'id_row' : 'id_row'+ str(cx),
                       'quantity' : row.quantity,
                       'amount' : row.amount})


    data = {
        'form':form,
        'order_title' : "Заказ номер такой-то",
        'number': order.number,
        'order_id': order.id,
        'client': order.client,
        'comment': order.comment,
        'phone': order.client.phone_number,
        'amount': order.amount,
        'type_pay': order.get_type_play_display(),
        'date':  order.date.strftime("%d.%m.%Y %H:%M"),
        'tabulars': tab_ls,
    }

    return render(request,'order_driver.html',data)

def procces_order(request):
    if request.method == 'POST':
        param = request.POST
        order = Order.objects.filter(id=param['order_id']).first()
        order.comment = param['order_id']
        order.returned_container = param['returned_container']
        if param['status'] == 'delivered':
            order.status_order = Order.STATUS_TYPE_COMPLETED
        elif  param['status'] == 'postponed':
            order.status_order = Order.STATUS_TYPE_postponed

        # if param['data_table_1'] != '':
        #     row = TabluarOrders.objects.filter(order=order,id=1).first()
        #     row
        order.save()

        driver = Driver.objects.filter(user=request.user).first()
        if driver:
            orders = get_data_for_report(driver)
            data = {'driver': driver,
                    'orders': orders}
            return render(request, 'report_for_driver.html', data)


