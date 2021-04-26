# -*- coding: utf-8 -*-
import json
# from db_queries import get_client_address, get_client_name, add_line, transform_number, makes_initial_tables, makes_initial_tables_Pay, add_line_Orders, get_client_orders, get_address_coordinates, add_line_coordinates,makes_initial_tables_coordinates
import time
from builtins import range

import requests
from urllib import request
# import xlrd
# import pickle
import sqlite3
# conn = sqlite3.connect("C:\\Users\\Администратор\\PycharmProjects\\water\\db.sqlite3") # или :memory: чтобы сохранить в RAM
conn = sqlite3.connect("/home/yuriy/projects/water/db.sqlite3") # или :memory: чтобы сохранить в RAM
cursor = conn.cursor()

import datetime as DT
import calendar

# from interaction1C import  add_client_1c, get_last_zakaz_1c

api_url = 'http://127.0.0.1:8000'

APIUrl = 'https://api.green-api.com/waInstance7402/'
token = '0bbcb29ff60098202ffbb07df051131f21d2234d12c22c4ad4'

stringForImput = ['НАЧАТЬ', 'ЗАКАЗ', 'ЗАКАЗАТЬ', 'ORDER', 'ZAKAZ']

def add_client(data):
    headers = {
        'Content-Type': 'application/json'
    }

    address = data.street + 'д. ' + data.number_home

    payload = {
        "name": data.name,
        "phone_number": data.id,
        "address": address,
    }
    response = requests.request("POST", api_url + '/api/add_client/', headers=headers, data=json.dumps(payload))

    client_data = json.loads(response.text)

    return client_data.get('id')

    # print(response.text)
    # # Вставляем данные в таблицу
    # sql = '''INSERT INTO common_client ('name','phone_number','address') VALUES (?, ?, ?)'''
    # cursor.execute(sql, (data.name, data.id, address))
    # conn.commit()
    # return 'успех'



def get_amount(client):
    sum = 0
    for row in client.cart:
        sum += row.get('summa')
    return sum

def get_client(number):
    client = requests.get(api_url + '/api/get_client/'+number+'/')
    if client.text:
        return json.loads(client.text)
    # sql = "SELECT * FROM common_client WHERE phone_number=?"
    # cursor.execute(sql, [(number)])
    # for row in cursor.fetchall():
    #     return row

def read_sql(sql):
    path = 'DataAddress\settings.xls'
    cursor.execute(sql)
    l = []
    for row in cursor.fetchall():
        l.append(row)
    return l

# positions_alt = read_sql("select * from common_positions")
positions = requests.get(api_url + '/api/positions/')
if positions.text:
    positions = json.loads(positions.text)

# gardens = read_sql("select * from common_gardens")
gardens = requests.get(api_url + '/api/gardens/')

# dist_coef = read_sql("select * from common_gardens")

# districtsSP = read_sql(3)

# districts_alt = read_sql("select del.name as district, dri.name as driver from common_delevirydistricts del left join common_driver dri ON del.driver_id = dri.id")
districts = requests.get(api_url + '/api/districts/')
if districts.text:
    districts = json.loads(districts.text)

# streets_alt = read_sql("select * from common_streets")
# streets = requests.get('https://almaz-water.herokuapp.com/api/streets/')
# if streets.text:
#     streets = json.loads(streets.text)

def add_zakaz(client):

    headers = {
        'Content-Type': 'application/json'
    }
    tabulars = []
    summadoc = 0
    for row in client.cart:
        summadoc += row['summa']
        d = {
            "price": row['summa']/row['count'],
            "quantity": row['count'],
            "amount": row['summa'],
            "order": 1,
            "position": row['position_id']
        }
        tabulars.append(d)

    payload = {
        "client": client.pk,
        "amount": summadoc,
        "tabulars": tabulars,
    }

    response = requests.request("POST", api_url +'/api/add_order/', headers=headers, data=json.dumps(payload))

    # number = read_sql('select  id from documents_order order by  number DESC limit 1')
    # if number[0]:
    #     cur_number = number[0][0] + 1
    # else:
    #     cur_number = 1
    # date = DT.datetime.now()
    # client_id = client.id
    # amount = get_amount(client)
    # # Вставляем данные в заказ
    # sql = '''INSERT INTO documents_order ('number','date','client_id', 'amount') VALUES (?, ?, ?, ?)'''
    # result1 = cursor.execute(sql, (cur_number, date, client.pk, amount))
    # conn.commit()
    #
    # for row in client.cart:
    #     sql = '''INSERT INTO documents_tabluarorders ('order_id','position_id','quantity', 'price', 'amount') VALUES (?, ?, ?, ?, ?)'''
    #     price = row.get('summa') / row.get('count')
    #     cursor.execute(sql, (cur_number, row.get('position_id'), row.get('count'), price, row.get('summa')))
    #     conn.commit()
    #     time.sleep(1)

    return 'успех'

def get_coordinats_yandex(line_address):

    headers = {'Content-Type': 'application/json', 'Accept-Encoding': None, 'Authorization': 'Basic'}
    url = 'https://geocode-maps.yandex.ru/1.x/?apikey=9461304f-c5d2-425e-abcb-e705742a6569&geocode=' + line_address + '&format=json'
    res = requests.get(url=url,headers=headers)
    return json.loads(res.text)

def action_yandex(dataStreet,client,self,text,id):
    alpha = dataStreet['response']['GeoObjectCollection']['metaDataProperty']['GeocoderResponseMetaData']
    if alpha.get('suggest') == None:
        # В названии улицы нет ошибок
        client.street = text
        client.steps.append(['specify_street', '', specify_number_home])
        client.size_Menu = 0
        return self.send_message(id, 'Укажите номер дома, если есть корпус, то укажите через "/"(слеш):')
    else:
        # Получаем исправленное название улицы
        nameStreet = alpha.get('suggest')
        nameFixStreet = nameStreet.replace('Актюбинская область Актюбинск', '').replace('<fix>', '').replace('</fix>',
                                                                                                             '').lstrip()

        client.street = nameFixStreet
        client.steps.append(['specify_street', '', specify_number_home])
        client.size_Menu = 0
        return self.send_message(id, 'Укажите номер дома, если есть корпус, то укажите через "/"(слеш):')

def back_menu(*args):
    self, client, text, id = args[0]['self'], args[0]['client'], args[0]['text'], args[0]['id'],

    if client.steps[-1][0] == 'contacts' or client.steps[-1][0] == 'promo' or client.steps[-1][0] == 'info_company':
        return info(*args)

    elif client.steps[-1][0] == 'new_client' or client.steps[-1][0] == 'make_an_order' or client.steps[-1][0] == 'info' or client.steps[-1][0] == 'create_order':
        return start(*args)

    elif client.steps[-1][0] == 'specify_date' or client.steps[-1][0] == 'soon_delevery':
        return delevery_time(*args)

    elif client.steps[-1][0] == 'paymont_cash' or client.steps[-1][0] == 'paymont_online':
        return soon_delevery(*args)

    elif client.steps[-1][0] == 'delevery_time' or client.steps[-1][0] == 'add_pos':
        return make_an_order(*args)

    elif client.steps[-1][0] == 'infoCart':
        return start(*args)
    # elif client.steps[-1][0] == 'soon_delevery':
    #     return delevery_time(*args)

def specify_date(*args):
    self, id, client, text = args[0]['self'], args[0]['id'], args[0]['client'], args[0]['text']
    client.steps.append(['specify_date', '', soon_delevery])
    client.size_Menu = 0
    string = 'Укажите удобную дату доставки \nформат: 20.01.21\n -----------------------------\n(0.Назад)'
    return self.send_message(id, string)


# def specify_time(*args):
#     self, id, client, text = args[0]['self'], args[0]['id'], args[0]['client'], args[0]['text']
#
#     check =  check_date(client,text)
#     if check != None:
#         return self.send_message(id, check)
#
#     client.steps.append(['specify_time', '', soon_delevery])
#     client.size_Menu = 0
#     string = 'Укажите время в формате: 12:30'
#     return self.send_message(id, string)
#

def check_date(client, DateTime):

    try:
        date = DT.datetime.strptime(DateTime, '%d.%m.%y').date()
        cdate = DT.datetime.now()
        countDaycurr = calendar.monthrange(cdate.year, cdate.month)  # get count day from current mounth
        if cdate.year != date.year:
            return 'Год указан не верно!\n Укажите дату заново!'
        if cdate.month != date.month:
            return 'Месяц указан не верно!\n Укажите дату заново!'
        if cdate.day > date.day and cdate.day != countDaycurr:
            return 'День указан не верно!\n Укажите дату заново!'
        elif cdate.day == date.day and cdate.hour > 22:  # Если день сегодняшний, но время уже ближе к концу дня
            return 'На текущий день заявки принемаются только до 22 часов!\n Укажите другую дату'

        client.date_of_delivery = DateTime
    except:
        return 'Неправильный формат даты! \n Укажите дату в формате: 01.01.21'

def control(*args):
    self, id, client, text = args[0]['self'], args[0]['id'], args[0]['client'], args[0]['text']
    if len(text) == 0 or (
            len(client.steps) != 0 or not str(text[0]).upper() in stringForImput) and client.size_Menu != 0 and not \
    text[
        0].isdigit():
        return f'Некорректная команда! Укажите команду цифрами'

    if client.size_Menu != 0 and client.size_Menu < int(text[0]):
        return f'Некорректная команда! Укажите команду от 1 до {client.size_Menu}'

    if len(client.steps) == 0 and not str(text).upper() in stringForImput:
        # name = client.name
        return 'Для начала заказа введите команду "Заказ"'


    return ''


def new_client(*args):
    self, client, id, text = args[0]['self'], args[0]['client'], args[0]['id'], args[0]['text']
    # client.steps.append(['make_an_order', '', lastMenu])
    client.size_Menu = 0
    return self.send_message(id, 'Спасибо! В ближайшее время с Вами свяжется наш менеджер.')

def delevery_time(*args):
    self, client, id, text = args[0]['self'], args[0]['client'], args[0]['id'], args[0]['text']
    client.steps.append(['delevery_time', '', delevery_timeM])
    client.size_Menu = len(delevery_timeM)
    return self.send_message(id, 'Выберите удобное время доставки:\n' + self.convert_to_string(delevery_timeM))

def make_an_order(*args):
    '''проверка наличие номера в базе данных '''
    self, client, id, text = args[0]['self'], args[0]['client'], args[0]['id'], args[0]['text']
    if client.name:
        return create_order(*args)
    else: # Регистрация нового клиента
        return registration_client(*args)
        # client.steps.append(['make_an_order', '', new_client])
        # client.size_Menu = 0
        # return self.send_message(id, 'Укажите ваше имя и номер телефона')

def registration_client(*args):
    self, client, id, text = args[0]['self'], args[0]['client'], args[0]['id'], args[0]['text']

    client.steps.append(['registration_client', '', registrM])
    client.size_Menu = len(registrM)
    return self.send_message(id, 'Выбирите тип клиента:\n' + self.convert_to_string(
        registrM))

def privatePerson(*args):
    self, client, id, text = args[0]['self'], args[0]['client'], args[0]['id'], args[0]['text']
    client.type = 'private'
    client.size_Menu = 0
    client.steps.append(['privatePerson', '', get_name_client])
    return self.send_message(id, 'Укажите Ваше Имя:\n')

def company(*args):
    self, client, id, text = args[0]['self'], args[0]['client'], args[0]['id'], args[0]['text']
    client.type = 'company'
    client.size_Menu = 0
    client.steps.append(['company', '', name_company])
    return self.send_message(id, 'Укажите название компании:\n')

def name_company(*args):
    self, client, id, text = args[0]['self'], args[0]['client'], args[0]['id'], args[0]['text']
    client.company = text
    client.name = text
    client.size_Menu = 0
    client.steps.append(['name_company', '', name_contact_company])
    return self.send_message(id, 'Укажите Имя контактного лица:\n')

def name_contact_company(*args):
    self, client, id, text = args[0]['self'], args[0]['client'], args[0]['id'], args[0]['text']
    client.contactPerson = text
    client.size_Menu = 0
    client.steps.append(['name_contact_company', '', phone_contactPerson])
    return self.send_message(id, 'Укажите телефон контактного лица:\n')

def phone_contactPerson(*args):
    self, client, id, text = args[0]['self'], args[0]['client'], args[0]['id'], args[0]['text']
    client.phoneContactPerson = text
    client.size_Menu = 0
    return select_district(*args)

def get_name_client(*args): # HERE give address
    self, client, id, text = args[0]['self'], args[0]['client'], args[0]['id'], args[0]['text']
    client.name = text
    return select_district(*args)

def select_district(*args):
    self, client, id, text = args[0]['self'], args[0]['client'], args[0]['id'], args[0]['text']
    t = 'Выберите Ваш район из списка: \n'

    command = {}
    t += str(1) + '. ' + "Садоводческий коллектив" + '\n'
    command["1"] = {'commandName': "Садоводческий коллектив"}
    for cx, l in enumerate(districts):
        t += str(cx + 2) + '. ' + l['name']  + '\n'
        command[str(cx + 2)] = {'district': l['name'] ,
                                # 'cost_of_delivery': districts.get(l[2])['cost_of_delivery'],
                                # 'free': districts.get(l[2])['free'],
                                'driver': l['driver'],
                                }
    t += '0. Назад.' + '\n'
    client.size_Menu = cx + 2
    client.steps.append(['select_district', command, get_user_address])
    self.send_message(id, t)

def get_user_address(*args):
    self, id, client, text = args[0]['self'], args[0]['id'], args[0]['client'], args[0]['text']
    client.address_in_base = True
    # if text == '0':
    #     return identification_by_address(*args)
    # elif text == '1': # Садоводческий коллектив
    #     # client.steps.append(['specify_address', '', specify_street])
    #     return specify_garden(*args)

    client.district = client.steps[-1][1].get(text)
    client.size_Menu = 0
    client.steps.append(['specify_address', '', specify_street])
    return self.send_message(client.id, 'Укажите улицу доставки, если нет улицы, то просто "0":')

def specify_street(*args):
    self, id, client, text = args[0]['self'], args[0]['id'], args[0]['client'], args[0]['text']

    if text == "0":
        client.street = client.district['district']
        client.steps.append(['process_street', '', specify_number_home])
        client.size_Menu = 0
        return self.send_message(id, 'Укажите номер дома, если есть корпус, то укажите через "/"(слеш):')

    line_address = 'Актюбинская область+Актюбинск+' + str(text)
    dataStreet = get_coordinats_yandex(line_address)
    if dataStreet.get('message') != 'Invalid key':
        return action_yandex(dataStreet,client,self,text,id)
    else:
        self.send_message('77071392125', 'Внимание! Сервис яндекса по подбору улицы не отработал!')
        self.send_message('77058370045', 'Внимание! Сервис яндекса по подбору улицы не отработал!')

def specify_number_home(*args):
    self, id, client, text = args[0]['self'], args[0]['id'], args[0]['client'], args[0]['text']
    client.number_home = text
    client.steps.append(['specify_number_home','', specify_number_apart])
    client.size_Menu = 0
    return self.send_message(id, 'Укажите номер квартиры, если нет, то просто "0":')

def specify_number_apart(*args):
    self, id, client, text = args[0]['self'], args[0]['id'], args[0]['client'], args[0]['text']
    if text != '0':
        client.number_apart = text
    client.pk = add_client(client)
    return create_order(*args)

def get_address(*args):
    self, client, id, text = args[0]['self'], args[0]['client'], args[0]['id'], args[0]['text']
    pass


def create_order(*args):
    self, client, id, text = args[0]['self'], args[0]['client'], args[0]['id'], args[0]['text']
    string = 'Выберите позицию из списка:\n'
    cx = 0
    for  pos in positions:
        cx += 1
        string += str(cx) + '. ' + pos['name'] + ' ' + str(pos['price']) + ' тенге.\n'

    client.steps.append(['create_order', '', get_count])
    client.size_Menu = len(positions)
    return self.send_message(id, string +'-----------------------------\n(0.Назад)')

def get_count(*args):
    self, client, id, text = args[0]['self'], args[0]['client'], args[0]['id'], args[0]['text']
    pos = positions[int(text)-1]

    if client.type and text == '1':
        string = 'Имеется ли у вас пустой бутыль в хорошем состоянии? Если да то вода по 500тг, если нет то выкупаете по 1500тг, и последующие заказы по 500 тг за выкупленный бутыль: \n1. Да 500тг.\n2. Нет 1500тг '
        client.steps.append(['get_count', pos, select_pos])
        client.size_Menu = 2
        return self.send_message(id, string)

    client.steps.append(['get_count', pos, add_pos])
    client.size_Menu = 0
    string = 'Укажите количество для позиции: "' + pos['name'] +'"\n'
    return self.send_message(id, string)

def select_pos(*args):
    self, id, client, text = args[0]['self'], args[0]['id'], args[0]['client'], args[0]['text']
    pos = client.steps[-1][1]
    if text == '2':
        pos['Price'] = 1500
    client.steps.append(['select_pos', pos, add_pos])
    client.size_Menu = 0
    string = 'Укажите количество для позиции: "' + pos[3] + '"\n'
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

def general(*args,textUser,menu=None):
    self, client, id, text = args[0]['self'], args[0]['client'], args[0]['id'], args[0]['text']
    client.steps.append(['delevery_time', '', delevery_timeM])
    client.size_Menu = len(delevery_timeM)
    return self.send_message(id, 'Выберите удобное время доставки:\n' + self.convert_to_string(delevery_timeM))


def contacts(*args):
    self, client, id, text = args[0]['self'], args[0]['client'], args[0]['id'], args[0]['text']
    client.steps.append(['contacts', '', ''])
    client.size_Menu = 0
    return self.send_message(id, 'Тут будут контактные данные для клиента...\n -----------------------------\n(0.Назад)')

def info_company(*args):
    self, client, id, text = args[0]['self'], args[0]['client'], args[0]['id'], args[0]['text']
    client.steps.append(['info_company', '', ''])
    client.size_Menu = 0
    return self.send_message(id, 'Тут будет информация для клиента...\n -----------------------------\n(0.Назад)')

def promo(*args):
    self, client, id, text = args[0]['self'], args[0]['client'], args[0]['id'], args[0]['text']
    client.steps.append(['promo', '', ''])
    client.size_Menu = 0
    return self.send_message(id, 'Тут будут акции для клиента...\n -----------------------------\n(0.Назад)')

def finish(*args):
    self, client, id, text = args[0]['self'], args[0]['client'], args[0]['id'], args[0]['text']
    client.steps.append(['finish', '', finish])
    client.size_Menu = 0
    return self.send_message(id, 'Спасибо! Ваш заказ принят! Для выполнения нового заказа введите команду "Заказть"')

def paymont_cash(*args):
    self, client, id, text = args[0]['self'], args[0]['client'], args[0]['id'], args[0]['text']
    client.steps.append(['finish', '', finish])
    client.size_Menu = 0
    add_zakaz(client)
    return self.send_message(id, 'Ваш заказ принят. Ожидайте доставку.')

def paymont_online(*args):
    self, client, id, text = args[0]['self'], args[0]['client'], args[0]['id'], args[0]['text']
    client.steps.append(['finish', '', finish])
    client.size_Menu = 0
    return self.send_message(id, 'Ваш заказ принят. после онлайн-оплаты будет передан на реализацию')

def info(*args):
    self, client, id, text = args[0]['self'], args[0]['client'], args[0]['id'], args[0]['text']
    client.steps.append(['make_an_order', 'backup', info_clientM])
    client.size_Menu = len(info_clientM)
    return self.send_message(id, 'Информация для клиентов:\n' + self.convert_to_string(
        info_clientM))

def start(*args):
    self, client, id, text = args[0]['self'], args[0]['client'], args[0]['id'], args[0]['text']
    if client.lastcart:
        menu = grandMenu
    else:
        menu = grandMenunoReplay

    client.steps.append(['make_an_order', 'backup',menu])
    client.size_Menu = len(menu)

    if len(client.steps) < 2:
        message = 'Вас приветствует компания "Алмаз"\n Выберите действие:\n' + self.convert_to_string(menu)
    else:
        message = ' Выберите действие:\n' + self.convert_to_string(menu)

    return self.send_message(id, message)

def soon_delevery(*args):
    self, client, id, text = args[0]['self'], args[0]['client'], args[0]['id'], args[0]['text']

    if text != '1':
        check = check_date(client, text)
        if check != None:
            return self.send_message(id, check)

    client.steps.append(['soon_delevery', '', paymentM])
    client.size_Menu = 0
    return self.send_message(id, 'Выберите способ оплаты:\n' + self.convert_to_string(paymentM))

def show_cart(*args):
    self, client, id = args[0]['self'], args[0]['client'], args[0]['id']
    infoCart = client.infoCart()
    return self.send_message(id, infoCart)

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
    client.steps.append(['editionCount', pos, show_cart])
    return self.send_message(id, infoCart)

def show_cart(*args):
    self, client, id = args[0]['self'], args[0]['client'], args[0]['id']
    infoCart = client.infoCart()
    return self.send_message(id, infoCart)

def get_position_by_code1C(code1C):
    for pos in positions:
        if pos['code1C'] == code1C:
            return pos
            break

def replay_cart(*args):
    self, client, id = args[0]['self'], args[0]['client'], args[0]['id']
    last_cart = client.lastcart #get_last_zakaz_1c(id)

    if last_cart:
        cx = 0
        message = 'В корзину добавлен:\n'
        for pos in last_cart.get('tabulars'):
            cx +=1
            Code1С = pos['position_data']['code1C']
            nomenklatura = pos['position_data']['name']
            psn = get_position_by_code1C(Code1С)
            summa = pos['quantity'] * psn['price']
            client.add_pos(position_id=pos['position_data']['id'],code1C=Code1С, position=nomenklatura, count=pos['quantity'], summa=summa)
            message += f'{cx}. {nomenklatura} цена: {psn["price"]} в количестве: {pos["quantity"]} штук на сумму: {summa} \n'
    else:
        message = 'Последний заказ в базе не найден.'

    client.steps.append(['replay_cart', "", myCartsMenu])
    client.size_Menu = len(myCartsMenu)
    return self.send_message(id, message+ '\n--------------------------\n' + self.convert_to_string(myCartsMenu))

    # if last_cart:
    #     return self.send_message(id, 'Корзина с товарами из крайнего заказа')
    # else:
    #     return self.send_message(id, 'Последний заказ в базе не найден.')

grandMenu   = {'1': {'name': 'Сделать заказ', 'method': make_an_order},  # меню выбора самого элемента
               '2': {'name': 'Информация для клиентов', 'method': info},
               '3': {'name': 'Повторить последний заказ', 'method': replay_cart},
               '4': {'name': 'Корзина', 'method': show_cart},
               }

grandMenunoReplay   = {'1': {'name': 'Сделать заказ', 'method': make_an_order},  # меню выбора самого элемента
               '2': {'name': 'Информация для клиентов', 'method': info},
               '3': {'name': 'Корзина', 'method': show_cart},
               }

registrM   = {'1': {'name': 'Частное лицо', 'method': privatePerson},  # меню выбора самого элемента
               '2': {'name': 'Компания', 'method': company},
               }



delevery_timeM = {'1': {'name': 'Ближайщее время.', 'method': soon_delevery},  # меню выбора самого элемента
                  '2': {'name': 'Указать свою дату', 'method': specify_date},
                  '0': {'name': 'Назад.', 'method': back_menu},
                    }

paymentM = {'1': {'name': 'Наличные', 'method': paymont_cash},  # меню выбора самого элемента
                  '2': {'name': 'Перевод Каспи', 'method': paymont_cash},
                  '3': {'name': 'Онлайн оплата', 'method': paymont_online},
                  '0': {'name': 'Назад.', 'method': back_menu},
                    }


info_clientM = {'1': {'name': 'Контактные данные', 'method': contacts},  # меню выбора самого элемента
                  '2': {'name': 'Данные о компании', 'method': info_company},
                  '3': {'name': 'Акции', 'method': promo},
                  '0': {'name': 'Назад.', 'method': back_menu},
                    }

successMenu = {'1': {'name': 'Завершить заказ', 'method': delevery_time},
               # После успешного добавление позиции в корзину
               '2': {'name': 'Главное меню', 'method': start},
               '3': {'name': 'Корзина', 'method': show_cart},
               '0': {'name': 'Назад', 'method': back_menu},
               }

myCartsMenu = {'1': {'name': 'Завершить заказ', 'method': delevery_time},
               # Меню когда находишься непосредственно в корзине
               '2': {'name': 'Главное меню', 'method': start},
               '3': {'name': 'Редактировать количество', 'method': edit_pos},
               }

class ClienOchag():
    def __init__(self, id):
        self.id = id
        dataclient = get_client(id)
        if dataclient:
            self.pk = dataclient['id']
            self.lastcart = self.last_cart()
            self.name = dataclient['name']
            self.Code1C =  dataclient['code1C']
        else:
            self.lastcart, self.name, self.pk, self.Code1C = None,'','',''
        # self.number = transform_number(id)
        self.type = ''
        self.company = ''
        self.contactPerson = ''
        self.phoneContactPerson = ''
        self.steps = []
        self.cart = []
        self.orders = []
        self.district = ''
        self.payment = ''
        # self.phone = transform_number(id)
        self.size_Menu = 0
        # self.distance = 0
        self.summaDostavki = 0
        self.date_of_delivery = ''
        self.time_of_delivery = ''
        self.number_apart = ''
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
        self.steps.append(['infoCart', '',myCartsMenu])
        return info + '____________________________________ \n' + f'ИТОГО: {str(summ)} тенге. \n' + self.convert_to_string(
            myCartsMenu)

    def convert_to_string(self, menu):
        ss = ''
        for s in menu.items():
            if isinstance(s[1], dict):
                ss += s[0] + '. ' + s[1]['name'] + '\n'
            else:
                ss += s[0] + '. ' + s[1] + '\n'
        return ss

    def add_pos(self,position_id, code1C, position, count, summa):

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
            # self.steps.append(['fine', '', after_order])
        else:
            self.steps = []

        self.cart = []
        # self.name = ''
        # self.address = ''
        # self.phone = ''
        self.payment = ''
        self.size_Menu = 0
        self.date_of_delivery = ''
        self.time_of_delivery = ''
        # self.number = ''

    def textFinish(self):

        s_int = self.get_total_summ()

        sss = str(s_int)
        summaDostavki = self.summaDostavki
        # return 'Ваш заказ принят, сумма заказа составляет ' + sss + ' тенге, тип оплаты: ' + self.payment + ', ожидайте доставку на адрес: ' + self.adress  # + '\n Ориентировачное время ожидания 40-60 минут'
        address = str(self.address)
        time_of_delivery = self.time_of_delivery
        note = self.note
            # self.orders.append(res.text)
        self.reset()
        return 'Заказ принят..'

    def last_cart(self):
        # sql = "select position_id, (select name from common_positions where common_positions.id=position_id) position,(select code1C from common_positions where common_positions.id=position_id) code1C,quantity, price, amount from documents_tabluarorders where order_id = (SELECT id FROM documents_order where client_id=? order by date desc limit 1)"
        # cursor.execute(sql, [(self.pk)])
        # l = []
        # for row in cursor.fetchall():
        #     l.append(row)
        # return l
        lastcart = requests.get(api_url+'/api/get_last_order/'+ self.id)
        if lastcart.text:
            lastcart = json.loads(lastcart.text)
        return lastcart

class WABot():
    def __init__(self, jsonM, clients, conn):
        if jsonM.get('messageData') == None:
            jsonMes = []
        else:
            jsonMes = jsonM['messageData']
        self.json = jsonM
        self.dict_messages = jsonMes
        # self.APIUrl = 'https://eu123.chat-api.com/instance181836/'
        # self.token = 'j1ia8lyacoqd2ofo'
        # self.APIUrl = 'https://api-whatsapp.io/api'
        # self.token = 'pn3s7k7neamdnw8y68hmmhcvhnt1nbjgxml7rf669c='
        self.APIUrl = APIUrl
        self.token = token

        # self.menu = data['menu']
        self.clients = clients
        self.Curr_clients = None
        self.curr_command = ''
        self.database = {'conn': conn,
                         }

    def send_requests(self, method, data):  # DEMODEMO demo
        print(data['body'])

        # url = "https://api.green-api.com/waInstance9102/sendMessage/710d9d92265ba34c1c8be98f5e490aafa63968a97c3b5caa5d"
        url = APIUrl + 'sendMessage/' + token

        payload = {"chatId": data['chatId'],
                   "message": data['body']}
        headers = {
            'Content-Type': 'application/json'
        }

        demo = self.debug
        if not demo:
            response = requests.request("POST", url, headers=headers, data=json.dumps(payload))


        return ''

    def send_message(self, chatID, text):
        data = {"chatId": chatID + '@c.us',
                "body": text}
        answer = self.send_requests('sendMessage', data)
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

    def processing(self,debug=False):
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

        params = {'self': self, 'client': client, 'id': id, 'text': text}

        if len(client.steps) == 0:
            return start(params)

        if text == '0' and client.steps[-1][0] != 'finish' and client.steps[-1][0] != 'specify_number_home' and client.steps[-1][0] != 'editionCount':
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
