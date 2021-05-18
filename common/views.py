from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from rest_framework.response import Response

from common.forms import LoginForm
from common.models import Client, Positions, Driver
from documents.models import Order, TabluarOrders

from django.db.models import Q

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
        if request.user.is_superuser:
            login(request, request.user)
            return redirect('/admin/')

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
    orders = Order.objects.filter(Q(client__driver=driver) | ~Q(status_order= Order.STATUS_TYPE_COMPLETED))
    data = []

    for inx, order in enumerate(orders):
        f = {'date':order.date,
         'client': order.client,
         'phone_number': order.client.phone_number,
         'type_pay': order.get_type_play_display(),
         'order': order,
         'order_id': order.id,
         'index': inx,
         'id_checkbox': 'id_checkbox_' + str(inx),
         'id_button': 'id_button_' + str(inx)
         }
        data.append(f)
    return data