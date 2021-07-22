# -*- coding: utf-8 -*-
import json
# import os
# import sys
# import configparser
import requests

import datetime as DT
import calendar
import socket

is_server = socket.gethostname() != 'yuriy-Aspire-5755G'
# config = configparser.ConfigParser()
# config.read('config.ini')
# 1
api_url = 'http://127.0.0.1:8000'
# api_url = 'https://water.hostman.site'
# api_url = 'https://almaz-water.herokuapp.com'

# 2
# APIUrl = 'https://api.green-api.com/waInstance7402/'
# token = '0bbcb29ff60098202ffbb07df051131f21d2234d12c22c4ad4'

APIUrl = 'https://api.green-api.com/waInstance9159/'
token = 'd089c99b960a312c819d2a8b67e2e6e81603d94c61bf095984'  # мой номер Тинькофф

# APIUrl = 'https://api.green-api.com/waInstance8073/'
# token = 'd017242c0e8f35dbe23616ebcdfb6241cb4ac18a1411f8d49d'

stringForImput = ['НАЧАТЬ', 'ЗАКАЗ', 'ЗАКАЗАТЬ', 'ORDER', 'ZAKAZ']


def get_amount(client):
    sum = 0
    for row in client.cart:
        sum += row.get('summa')
    return sum


def get_client(number):
    client = requests.get(api_url + '/api/get_client_full_data/' + number + '/')
    # client = requests.get(api_url + '/api/get_client/' + number + '/')
    if client.status_code == 201:
        return json.loads(client.text)


positions = requests.get(api_url + '/api/positions/')
if positions.text:
    positions = json.loads(positions.text)

gardens = requests.get(api_url + '/api/gardens/')

districts = requests.get(api_url + '/api/districts/')
if districts.text:
    districts = json.loads(districts.text)


def add_zakaz(client):
    headers = {
        'Content-Type': 'application/json'
    }
    tabulars = []
    summadoc = 0
    for row in client.cart:
        summadoc += row['summa']
        d = {
            "price": row['summa'] / row['count'],
            "quantity": row['count'],
            "amount": row['summa'],
            "order": 1,
            "position": row['position_id']
        }
        tabulars.append(d)

    payload = {
        "client": client.pk,
        "create_bot": True,
        # "type_play": type_pay,
        "new_client": client.new,
        "comment": client.comment,
        "amount": summadoc,
        "attention": client.attention,
        "date_dev": client.date_of_delivery,
        "tabulars": tabulars,
    }

    response = requests.request("POST", api_url + '/api/add_order/', headers=headers, data=json.dumps(payload))

    return 'успех'


def add_client(number_phone, address):
    headers = {
        'Content-Type': 'application/json'
    }

    payload = {
        "name": address,
        "address": address,
        "phone_number": number_phone,
    }

    response = requests.request("POST", api_url + '/api/add_client/', headers=headers, data=json.dumps(payload))

    return json.loads(response.text)


def back_menu(*args):
    self, client, text, id = args[0]['self'], args[0]['client'], args[0]['text'], args[0]['id'],

    # if client.steps[-1][0] == 'contacts' or client.steps[-1][0] == 'promo' or client.steps[-1][0] == 'info_company':
    #     return info(*args)

    if client.steps[-1][0] == 'create_order' and client.cart:
        return show_cart(*args)

    elif client.steps[-1][0] == 'new_client' or client.steps[-1][0] == 'make_an_order' or client.steps[-1][
        0] == 'info' or client.steps[-1][0] == 'create_order':
        return start(*args)

    elif client.steps[-1][0] == 'specify_date' or client.steps[-1][0] == 'soon_delevery':
        return show_cart(*args)

    # elif client.steps[-1][0] == 'paymont_cash' or client.steps[-1][0] == 'paymont_online':
    #     return soon_delevery(*args)

    elif client.steps[-1][0] == 'delevery_time' or client.steps[-1][0] == 'add_pos':
        return create_order(*args)

    elif client.steps[-1][0] == 'infoCart':
        return start(*args)

    elif client.steps[-1][0] == 'get_count':
        return create_order(*args)


def control(*args):
    self, id, client, text = args[0]['self'], args[0]['id'], args[0]['client'], args[0]['text']

    if len(text) == 0 or (
            len(client.steps) != 0 or not str(text).upper() in stringForImput) and client.size_Menu != 0 and not \
            text.isdigit():
        return f'Некорректная команда! Укажите команду цифрами'

    if client.size_Menu != 0 and client.size_Menu < int(text):
        return f'Некорректная команда! Укажите команду от 1 до {client.size_Menu}'

    if len(client.steps) == 0 and not str(text).upper() in stringForImput:
        # name = client.name
        return 'Для начала заказа введите команду "Заказ"'

    return ''


def new_client(*args):
    self, client, id, text = args[0]['self'], args[0]['client'], args[0]['id'], args[0]['text']
    client.steps.append(['finish', '', ''])
    client.size_Menu = 0
    dataclient = add_client(number_phone=id, address=text)
    client.pk = dataclient['id']
    client.lastcart = None
    client.name = dataclient['name']
    client.Code1C = ''
    client.address = dataclient['address']
    # client.new = False
    return create_order(*args)
    # message = 'Заяка на доставку от нового клиента:\n' + text
    # self.send_message('77071392125', message) # Указать номер менеджера для получения сообщений о новых клиентах.
    # self.send_message('77084713855', message) # Указать номер менеджера для получения сообщений о новых клиентах.
    # self.redis.set(id,'sleep', ex=17800)
    # return self.send_message(id, 'Спасибо! В ближайшее время с Вами свяжется наш менеджер.')


def specify_address(*args):
    self, id, client, text = args[0]['self'], args[0]['id'], args[0]['client'], args[0]['text']
    date_delevery = client.steps[-1][1][int(text) - 1].get('date')
    client.date_of_delivery = str(date_delevery)
    client.steps.append(['specify_address', '', control_address])
    client.size_Menu = 2
    if client.address:
        address = client.address
    else:
        address = client.name
    # self.logger.info(f'тест адрес доставки {id} -- {address}')
    return self.send_message(id, 'Адрес доставки: ' + address + '\n 1.Да \n 2.Нет')


def control_address(*args):
    self, id, client, text = args[0]['self'], args[0]['id'], args[0]['client'], args[0]['text']
    if text == '1':
        paymont_cash(*args)
    elif text == '2':
        client.attention = True
        client.size_Menu = 0
        client.steps.append(['control_address', '', other_address])
        self.read_chat = False
        return self.send_message(id, 'Укажите адрес доставки:')


def other_address(*args):
    self, id, client, text = args[0]['self'], args[0]['id'], args[0]['client'], args[0]['text']
    client.comment = text
    return paymont_cash(*args)


def read_chat(chatID):
    # url = "https://api.green-api.com/waInstance{{idInstance}}/readChat/{{apiTokenInstance}}"
    url = APIUrl + 'readChat/' + token

    payload = {"chatId": chatID + '@c.us',
               }
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text.encode('utf8'))


def delevery_time(*args):
    self, id, client, text = args[0]['self'], args[0]['id'], args[0]['client'], args[0]['text']
    list_dates = get_list_dates(client)
    # client.steps.append(['specify_date', list_dates, soon_delevery])
    client.steps.append(['specify_date', list_dates, specify_address])
    client.size_Menu = len(list_dates)
    string_list = ''
    for pos in list_dates:
        string_list += pos['date_view']
    string = 'Укажите удобную дату доставки:\n' + string_list + '-----------------------------\n(0.Назад)'
    return self.send_message(id, string)


def get_list_dates(client):
    # todo тут нужно сделать проверку на возможность доставки на эту дату
    # До 11 можно не сегодня принять, после только на завтра(если завтра не воскресенье)
    # Так же, делаем проверку по загруженности водителя на конкретный день.
    if client.dataclient and client.dataclient.get('open_orders'):
        open_orders = client.dataclient['open_orders'] if client.dataclient != None else 0
    else:
        open_orders = 0
    if client.dataclient and client.dataclient.get('plane'):
        plane = client.dataclient['plane'] if client.dataclient != None else 0
    else:
        plane = 0

    list = []
    cx = 0
    current_date = DT.date.today()
    # Проверка, если после 11 часов, то убираем сегодняшнюю дату
    current_time = DT.datetime.now()
    # print('current time: ',str(current_time))
    if is_server:  # Если это сервер, то время проверки доставки на сегодня +5 часов
        # hour_x = 11 + 5
        hour_x = 6
    else:
        hour_x = 11
    if current_time.hour < hour_x:  # and not client.new:
        # if False :
        start = 0
    else:
        start = 1

    # print('до get_list_dates цикла периода')
    for day in range(start, 10):
        row_date = current_date + DT.timedelta(days=day)
        # Проверка, если уже на этот день заказов выше нормы(plane)
        if not client.new and open_orders != None and open_orders != 0:
            if open_orders.get(str(row_date)) and open_orders[str(row_date)] >= plane:
                continue
        if row_date.isoweekday() != 7:  # exception sunday
            cx += 1
            date_view = f'{str(cx)}. ' + row_date.strftime('%d.%m.%y') + f' ({present_day(row_date)})\n'
            list.append({'num': cx,
                         'date': row_date,
                         'date_view': date_view,
                         })
    return list


def present_day(date):
    date_Day = date.isoweekday()
    if date_Day == 1:
        return 'понедельник'
    elif date_Day == 2:
        return 'вторник'
    elif date_Day == 3:
        return 'среда'
    elif date_Day == 4:
        return 'четверг'
    elif date_Day == 5:
        return 'пятница'
    elif date_Day == 6:
        return 'суббота'
    elif date_Day == 7:
        return 'воскресенье'


def create_order(*args):
    self, client, id, text = args[0]['self'], args[0]['client'], args[0]['id'], args[0]['text']

    if client.new and client.name == '':
        client.size_Menu = 0
        client.steps.append(['create_order', '', new_client])
        return self.send_message(id, 'Напишите Ваш адрес:')

    string = 'Выберите позицию из списка:\n'
    cx = 0
    for pos in positions:
        cx += 1
        string += str(cx) + '. ' + pos['name'] + ' ' + str(pos['price']) + ' тенге.\n'

    if client.cart:
        string += '(0.Назад)'
    client.steps.append(['create_order', '', get_count])
    client.size_Menu = len(positions)

    basement2 = '''
    ——————————————————
По каждой позиции заявка проводиться отдельно, и все товары Вы можете увидеть «КОРЗИНЕ». 
    '''

    return self.send_message(id, string + basement2)


def get_count(*args):
    self, client, id, text = args[0]['self'], args[0]['client'], args[0]['id'], args[0]['text']
    pos = positions[int(text) - 1]

    client.steps.append(['get_count', pos, add_pos])
    client.size_Menu = 50
    string = 'Укажите количество для позиции: "' + pos['name'] + '"\n'
    return self.send_message(id, string)


def select_pos(*args):
    self, id, client, text = args[0]['self'], args[0]['id'], args[0]['client'], args[0]['text']
    pos = client.steps[-1][1]
    if text == '2':
        pos['price'] += 1000
    client.steps.append(['select_pos', pos, add_pos])
    client.size_Menu = 0
    string = 'Укажите количество для позиции: "' + pos['name'] + '"\n'
    return self.send_message(id, string)


def add_pos(*args):
    self, id, client, text = args[0]['self'], args[0]['id'], args[0]['client'], args[0]['text']
    count = int(text)
    pos = client.steps[-1][1]
    position_id, code1C, nomenklatura, price = pos['id'], pos['code1C'], pos['name'], pos['price']
    summa = int(price) * int(count)
    client.add_pos(position_id, code1C, nomenklatura, count, summa)
    client.steps.append(['add_pos', client.steps[-1][1], successMenu])
    client.size_Menu = len(successMenu) - 1
    return self.send_message(id,
                             f'В корзину добавлен: {nomenklatura} цена: {price} в количестве: {count} штук на сумму: {summa} \n' + self.convert_to_string(
                                 successMenu))


def finish(*args):
    self, client, id, text = args[0]['self'], args[0]['client'], args[0]['id'], args[0]['text']
    client.steps.append(['finish', '', finish])
    client.size_Menu = 0
    self.redis.set(id, 'sleep', ex=36000)
    return self.send_message(id, 'Спасибо! Ваш заказ принят! Для выполнения нового заказа введите команду "Заказть"')


def paymont_cash(*args):
    self, client, id, text = args[0]['self'], args[0]['client'], args[0]['id'], args[0]['text']
    client.steps.append(['finish', '', specify_address])
    client.size_Menu = 0
    add_zakaz(client)
    finish_text = client.infoOffers()
    client.reset()
    if self.read_chat:
        read_chat(id)
    self.redis.set(id, 'sleep', ex=36000)
    return self.send_message(id, finish_text)


def welcome(*args):
    self, client, id, text = args[0]['self'], args[0]['client'], args[0]['id'], args[0]['text']

    # message = 'Здравствуйте! Вас приветствует Компания по доставке питьевой бутилированной воды ALMAZ SU 💧\nЧтобы сделать заказ отправьте цифру 1'
    if len(client.steps) > 0 and client.steps[-1][0] == 'welcome':
        message = 'Для продолжения нажмите 1'
    else:
        message = '''
            Здравствуйте! Вас приветствует Компания по доставке питьевой бутилированной воды ALMAZ SU 💧\nВыберите действие:\n1. Сделать заказ.\n2. Связаться с менеджером(до 17:30).
        \n————————————————-\n*(укажите команду цифрой 1 или 2)*\n
        ❗️❗️❗️Просим Вас Уважаемые клиенты отвечать Chat Botu по факту вопроса цифрами и Уведомляем о том что голосовые сообщения Bot не распознаёт!!!❗️❗️❗
        '''
    client.steps.append(['welcome', '', start])
    self.redis.hset('buzzy', id, int(DT.datetime.now().timestamp()))
    return self.send_message(id, message)


def contacts_menagers(*args):
    self, client, id, text = args[0]['self'], args[0]['client'], args[0]['id'], args[0]['text']
    text = 'Для связи с менеджером свяжитесь по номерам:\n +7 708 471 38 11,\n +7 708 471 38 55'
    self.redis.set(id, 'sleep', ex=36000)
    return self.send_message(id, text)


def start(*args):
    self, client, id, text = args[0]['self'], args[0]['client'], args[0]['id'], args[0]['text']

    self.redis.hdel('buzzy', id)

    if text == '1':
        return create_order(*args)
    elif text == '2':
        return contacts_menagers(*args)
    else:
        self.redis.set(id, 'sleep', ex=36000)
        # return welcome(*args)


def edit_pos(*args):
    self, client, id = args[0]['self'], args[0]['client'], args[0]['id']
    if len(client.cart) == 1:
        return specify_quality(*args)
    client.steps.append(['edit', 'infoCart', specify_quality])
    client.size_Menu = len(client.cart)
    return self.send_message(id, 'Укажите номер позиции для редактирование количества')


def specify_quality(*args):
    self, id, client, text = args[0]['self'], args[0]['id'], args[0]['client'], args[0]['text']
    if len(client.cart) == 1:
        pos = client.cart[0]
    else:
        pos = client.cart[int(text[0]) - 1]

    client.steps.append(['editionCount', pos, edit_count])
    client.size_Menu = 0
    string = 'Укажите новое количество для позиции: ' + pos['position']
    return self.send_message(id, string)


def edit_count(*args):
    self, client, id, text = args[0]['self'], args[0]['client'], args[0]['id'], args[0]['text']
    pos = client.steps[-1][1]
    if text[0] == '0':
        client.cart.remove(pos)
    else:
        price = pos['summa'] / pos['count']
        pos['count'] = int(text[0])
        pos['summa'] = pos['count'] * price
    infoCart = client.infoCart()
    client.steps.append(['editionCount', pos, myCartsMenu])
    return self.send_message(id, infoCart)


def show_cart(*args):
    self, client, id = args[0]['self'], args[0]['client'], args[0]['id']
    infoCart = client.infoCart()
    client.steps.append(['show_cart', '', myCartsMenu])
    return self.send_message(id, infoCart)


def get_position_by_code1C(code1C):
    for pos in positions:
        if pos['code1C'] == code1C:
            return pos
            break


def replay_cart(*args):
    self, client, id = args[0]['self'], args[0]['client'], args[0]['id']
    last_cart = client.lastcart  # get_last_zakaz_1c(id)

    if last_cart:
        cx = 0
        message = 'В корзину добавлен:\n'
        for pos in last_cart.get('tabulars'):
            cx += 1
            Code1С = pos['position_data']['code1C']
            nomenklatura = pos['position_data']['name']
            psn = get_position_by_code1C(Code1С)
            summa = pos['quantity'] * psn['price']
            client.add_pos(position_id=pos['position_data']['id'], code1C=Code1С, position=nomenklatura,
                           count=pos['quantity'], summa=summa)
            message += f'{cx}. {nomenklatura} цена: {psn["price"]} в количестве: {pos["quantity"]} штук на сумму: {summa} \n'
    else:
        message = 'Последний заказ в базе не найден.'

    client.steps.append(['replay_cart', "", myCartsMenu])
    client.size_Menu = len(myCartsMenu)
    return self.send_message(id, message + '\n--------------------------\n' + client.convert_to_string(myCartsMenu))


grandMenu = {'1': {'name': 'Сделать заказ', 'method': create_order},  # меню выбора самого элемента
             #  '2': {'name': 'Информация для клиентов', 'method': info},
             '2': {'name': 'Повторить последний заказ', 'method': replay_cart},
             '3': {'name': 'Корзина', 'method': show_cart},
             }

grandMenu2 = {'1': {'name': 'Дополнить заказ', 'method': create_order},  # меню выбора самого элемента
              #   '2': {'name': 'Информация для клиентов', 'method': info},
              '2': {'name': 'Повторить последний заказ', 'method': replay_cart},
              '3': {'name': 'Корзина', 'method': show_cart},
              }

grandMenunoReplay = {'1': {'name': 'Сделать заказ', 'method': create_order},  # меню выбора самого элемента
                     # '2': {'name': 'Информация для клиентов', 'method': info},
                     '2': {'name': 'Корзина', 'method': show_cart},
                     }

grandMenunoReplay2 = {'1': {'name': 'Дополнить заказ', 'method': create_order},  # меню выбора самого элемента
                      # '2': {'name': 'Информация для клиентов', 'method': info},
                      '2': {'name': 'Корзина', 'method': show_cart},
                      '3': {'name': 'Завершить заказ', 'method': delevery_time},
                      }

successMenu = {'1': {'name': 'Завершить заказ', 'method': delevery_time},
               '2': {'name': 'Дополнить заказ', 'method': create_order},
               # После успешного добавление позиции в корзину
               # '3': {'name': 'Главное меню', 'method': start},
               '3': {'name': 'Корзина', 'method': show_cart},
               '0': {'name': 'Назад', 'method': back_menu},
               }

myCartsMenu = {
    '1': {'name': 'Редактировать количество', 'method': edit_pos},
    '2': {'name': 'Дополнить заказ', 'method': create_order},
    '3': {'name': 'Завершить заказ', 'method': delevery_time},
}


class ClienOchag():
    def __init__(self, id):
        self.id = id
        self.lastcart = None
        self.comment = ''
        self.attention = False
        dataclient = get_client(id)
        if not dataclient or dataclient.get('client_id') == 'None':
            self.new = True
            self.name = ''
        else:
            self.new = False
            self.address = ''

            self.pk = dataclient['client_id']
            self.lastcart = dataclient['last_order']
            self.name = dataclient['client_name']
            self.Code1C = dataclient['client_code1C']
            self.address = dataclient['client_address']

        self.dataclient = dataclient
        self.steps = []
        self.cart = []
        self.orders = []
        self.payment = ''
        self.size_Menu = 0
        self.summaDostavki = 0
        self.date_of_delivery = ''
        self.time_of_delivery = ''
        self.note = ''

    def infoCart(self):

        if len(self.cart) == 0:
            self.steps.append(['infoCart', 'empty', back_menu])
            self.size_Menu = 1
            return 'Ваша корзина пуста! \n 1. Вернуться в главное меню \n 0. Назад'

        cx = 0
        info = 'Ваша корзина: \n'
        summ = 0
        for pos in self.cart:
            cx += 1
            summ += pos['summa']
            info += str(cx) + '. ' + pos['position'] + ' ' + str(pos['count']) + ' штук(и) ' + str(
                pos['summa']) + ' тенге \n'

        self.size_Menu = len(myCartsMenu)
        self.steps.append(['infoCart', '', myCartsMenu])
        return info + '____________________________________ \n' + f'ИТОГО: {str(summ)} тенге. \n' + self.convert_to_string(
            myCartsMenu)

    def infoOffers(self):

        # if len(self.cart) == 0:
        #     self.steps.append(['infoCart', 'empty', back_menu])
        #     self.size_Menu = 1
        #     return 'Ваша корзина пуста! \n 1. Вернуться в главное меню \n 0. Назад'

        cx = 0
        info = 'Ваш заказ принят: \n'
        summ = 0
        for pos in self.cart:
            cx += 1
            summ += pos['summa']
            info += str(cx) + '. ' + pos['position'] + ' ' + str(pos['count']) + ' штук(и) ' + str(
                pos['summa']) + ' тенге \n'

        self.size_Menu = len(myCartsMenu)
        self.steps.append(['infoCart', '', myCartsMenu])
        address = self.address
        dateV = self.date_of_delivery
        dateDev = self.date_of_delivery[8:10] + '.' + self.date_of_delivery[5:7] + '.' + self.date_of_delivery[:4]
        text = info + '____________________________________ \n' + f'ИТОГО: {str(summ)} тенге. \nАдрес доставки: {address}\nЖелаемая дата доставки: {dateDev}'
        if self.comment:
            text += f'\nКомментарий: {self.comment}'
        return text

    def convert_to_string(self, menu):
        ss = ''
        cx = 0
        for s in menu.items():
            # Проверяем, если в корзине еще нет товаров, то команду "Корзина" пользователю не показываем.
            if s[1]['name'] == 'Корзина' and not self.cart:
                continue

            cx += 1
            if isinstance(s[1], dict):
                ss += s[0] + '. ' + s[1]['name'] + '\n'
            else:
                ss += s[0] + '. ' + s[1] + '\n'

        self.size_Menu = cx
        return ss

    def add_pos(self, position_id, code1C, position, count, summa):

        new = True
        for i in self.cart:
            if i['code1C'] == code1C:
                i['count'] += count
                i['summa'] += summa
                new = False

        if new:
            data = {'position': position,
                    'position_id': position_id,
                    'code1C': code1C,
                    'count': count,
                    'summa': summa,
                    }
            self.cart.append(data)

    def reset(self):

        if self.steps[-1] == 'fine' or self.steps[-1][0] == 'fine' or self.steps[-1][0] == 'after_order':
            self.steps = []
        else:
            self.steps = []

        self.cart = []
        self.payment = ''
        self.size_Menu = 0
        self.date_of_delivery = ''
        self.time_of_delivery = ''


class WABot():
    def __init__(self, jsonM, clients, logger, redis):
        if jsonM.get('messageData') == None:
            jsonMes = []
        else:
            jsonMes = jsonM['messageData']
        self.json = jsonM
        self.dict_messages = jsonMes
        self.APIUrl = APIUrl
        self.token = token
        self.clients = clients
        self.Curr_clients = None
        self.curr_command = ''
        self.logger = logger
        self.read_chat = True
        self.redis = redis

    def send_requests(self, method, data):  # DEMODEMO demo
        print(data['body'])

        url = APIUrl + 'sendMessage/' + token

        payload = {"chatId": data['chatId'],
                   "message": data['body']}
        headers = {
            'Content-Type': 'application/json'
        }

        demo = self.debug
        if not demo:
            response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
            self.logger.debug(f"{data['chatId']} - {data['body']}")

        return ''

    def send_message(self, chatID, text):
        data = {"chatId": chatID + '@c.us',
                "body": text}
        answer = self.send_requests('sendMessage', data)
        # self.logger.debug(f"{chatID} - {text}")
        return answer

    def convert_to_string(self, menu):
        ss = ''
        for s in menu.items():

            if isinstance(s[1], dict):
                ss += s[0] + '. ' + s[1]['name'] + '\n'
            else:
                ss += s[0] + '. ' + s[1] + '\n'
        return ss

    def identification(self, id):
        client = self.clients.get(id)
        if client == None:
            client = ClienOchag(id)
            self.clients[id] = client
        self.curr_client = client

    def processing(self, debug=False):
        self.debug = debug
        if self.json['messageData']:
            text = self.json['messageData']['textMessageData']['textMessage']
            id = self.json['senderData']['chatId']
            id = id.replace('@c.us', '')
            print(id, text)
            self.identification(id)
            # try:
            return self.get_command(id, text)

    def get_command(self, id, text):
        client = self.curr_client

        # //*// Если это количество, то убираем все кроме цифр, потомучто клиенты любят писать 2 бут. 3 бутылки
        if len(client.steps) != 0 and client.steps[-1][0] == 'get_count':
            a = ''.join([i for i in text if i.isdigit()])
            text = a

        params = {'self': self, 'client': client, 'id': id, 'text': text}

        if len(client.steps) == 0:
            return welcome(params)

        if client.steps[-1][0] == 'finish':
            return ''

        if text == '0' and client.steps[-1][0] != 'finish' and client.steps[-1][0] != 'specify_number_home' and \
                client.steps[-1][0] != 'editionCount':
            return back_menu(params)

        text_control = control(params)
        if not text_control == '':
            return self.send_message(id, text_control)

        if str(text).upper() in stringForImput:  # Точка входа
            return start(params)

        else:
            if isinstance(client.steps[-1][2], dict):
                return client.steps[-1][2].get(text)['method'](params)
            else:
                return client.steps[-1][2](params)
