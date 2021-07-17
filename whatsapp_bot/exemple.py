a = 5
b = 1

try:
    c = a / b
except:
    try:
       print('1 фаза')
       с = a / b
       print('1,5 фаза')
    except:
        print('2 фаза')