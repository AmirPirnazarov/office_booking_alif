from datetime import *


# Создаем список где будут хронятся данные для обработки
input_person = []


def cabinet_selection():
    while True:
        cabin = input("Выберете кабинет который хотите забронировать: 1...5\n")
        try:
            if int(cabin) in range(1, 6):
                print("True")
                break
            else:
                print("error!!! Выберете правельный кабинет! от 1 до 5. СПАСИБО! \n")
        except ValueError:
            print("Вы вводите что-то не то!\n")


cabinet_selection()