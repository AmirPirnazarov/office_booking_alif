from datetime import *
import pymysql.cursors

# Подключение к БД MySQL
try:
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 db='booking',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    print("connect on BD successful!!")
except pymysql.err.OperationalError:
    print("not connection on BD!!")
    exit(0)

# Создаем список где будут хронятся данные для обработки
input_person = []

# Берем сегоднешнию дату и форматируем под нашу задачу
date_now = date.today()
format_day = date_now.strftime("%Y-%m-%d")
format_year = date_now.strftime("%Y")
f_d = datetime.strptime(format_day, "%Y-%m-%d")


def cabinet_selection():
    while True:
        cabin = input("Выберете кабинет который хотите забронировать: 1...5\n")
        try:
            if int(cabin) in range(1, 6):
                input_person.append(cabin)
                break
            else:
                print("error!!! Выберете правельный кабинет! от 1 до 5. СПАСИБО! \n")
        except ValueError:
            print("Вы вводите что-то не то!\n")


# Функция которая принимает дату и время бронирования
def time_and_date_selection():
    while True:
        date_time = input("Введите дату и время когда хотите Забронировать? 07-15 12:00\n")
        try:
            if int(date_time[0:2]) <= 12 and date_time[2:3] == "-" and int(date_time[3:5]) <= 31:
                if int(date_time[6:8]) <= 24 and date_time[8:9] == ":" and int(date_time[9:11]) <= 59:
                    date_time_format = datetime(month=int(date_time[0:2]), day=int(date_time[3:5]), year=int(format_year))
                    if date_time_format >= f_d:
                        input_person.append(date_time)
                        break
                    else:
                        print("Error!!! Вы выбрали день в прошлом \n")
                else:
                    print("Error!!! Выберете правельное время! например - 15:30. СПАСИБО! \n")
            else:
                print("Error!!! Выберете правельное день недели! например - 05-23. СПАСИБО! \n")

        except ValueError:
            print("Вы вводите что-то не то!")


# Функция принимает на сколько часов бронируется кабинет
def hours_selection():
    while True:
        hours = input("продолжительность брони(час-минуты)? н.р 01:20 или 00:40 \n")
        try:
            if int(hours[0:2]) <= 23 and int(hours[3:5]) <= 59 and hours[2:3] == ":":
                input_person.append(hours)
                break
            else:
                print("НЕВЕРНО!!! Выберете правельную дату! сначала месяц потом день недели \n")
        except ValueError:
            print("Вы вводите что-то не то!")


cabinet_selection()
time_and_date_selection()
hours_selection()
print(input_person)