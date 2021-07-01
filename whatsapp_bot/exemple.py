"""Цель: Нам нужен период с вчерашего 17.30 по сегодняшний 8. 30
 Получение даты начало:
  1.Получаем текущую дату
  2. Отнимаем день.
  3. Приравниваем полученную дату к 17.30

  Получение даты окончание:
  1. Текушую дату приравниваем к 8.30
"""
from datetime import date
from datetime import datetime, timedelta
from datetime import time

dt1_begin = datetime.combine(date.today() - timedelta(days=1), time(17, 30, 00))
dt1_finish = datetime.combine(date.today(), time(8, 30, 00))
dt2_finish = datetime.combine(date.today(), time(17, 30, 00))
print(dt1_begin)