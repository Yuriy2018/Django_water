from .models import TabluarOrders

from django.db.models import F, QuerySet, Sum, Count

def getData(general, status, date_dev, start='', finish='', status_order='1'):

    if general:
        if status == '1':
            data = TabluarOrders.objects.values(date_dev=F('order__date_dev'),
                                                driver=F('order__client__driver__name'),
                                                district=F('order__client__district__name'),
                                                address=F('order__client__name'),
                                                phone_number=F('order__client__phone_number'),
                                                position_=F('position__name'),
                                                quantity_=F('quantity'),
                                                amount_=F('amount'),
                                                comment=F('order__comment')
                                                ).filter(order__date_dev=date_dev).order_by('driver', 'district')
        else:
            data = TabluarOrders.objects.values(date_dev=F('order__date_dev'),
                                                driver=F('order__client__driver__name'),
                                                district=F('order__client__district__name'),
                                                address=F('order__client__name'),
                                                phone_number=F('order__client__phone_number'),
                                                position_=F('position__name'),
                                                quantity_=F('quantity'),
                                                amount_=F('amount'),
                                                comment=F('order__comment')
                                                ).filter(order__date_dev=date_dev, order__status_order=status_order,
                                                         ).order_by(
                'driver', 'district')


    elif status == '1':
        data = TabluarOrders.objects.values(date_dev=F('order__date_dev'),
                                            driver=F('order__client__driver__name'),
                                            district=F('order__client__district__name'),
                                            address=F('order__client__name'),
                                            phone_number=F('order__client__phone_number'),
                                            position_=F('position__name'),
                                            quantity_=F('quantity'),
                                            amount_=F('amount'),
                                            comment=F('order__comment')
                                            ).filter(order__date_dev=date_dev, order__date__gte=start,order__date__lte=finish).order_by('driver','district')
    else:
        data = TabluarOrders.objects.values(date_dev=F('order__date_dev'),
                                            driver=F('order__client__driver__name'),
                                            district=F('order__client__district__name'),
                                            address=F('order__client__name'),
                                            phone_number=F('order__client__phone_number'),
                                            position_=F('position__name'),
                                            quantity_=F('quantity'),
                                            amount_=F('amount'),
                                            comment=F('order__comment')
                                            ).filter(order__date_dev=date_dev, order__status_order=status_order, order__date__gte=start,order__date__lte=finish).order_by('driver', 'district')
    return data