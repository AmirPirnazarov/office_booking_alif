from datetime import *


# Создаем список где будут хронятся данные для обработки
input_person = []


def cabinet_selection():
    cabin = int(input("Выберете кабинет который хотите забронировать: 1...5"))
    if cabin in range(1, 6):
        print(True)
    else:
        cabinet_selection()


cabinet_selection()