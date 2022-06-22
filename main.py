from datetime import *
import pymysql.cursors
try:  # Проверяем методом исключения подключение к БД MySQL
    connection = pymysql.connect(host='localhost',  # Имя хоста
                                 user='root',  # Имя пользоватеся
                                 db='booking',  # Название Базы данных
                                 charset='utf8mb4',  # Кодировка
                                 cursorclass=pymysql.cursors.DictCursor) # Выбираем класс для подключ
    print("connect on BD successful!!")  # Выводим что успешко подключился
except pymysql.err.OperationalError:
    print("not connection on BD!!") # Если не подключенно то выводит следующее сообщение! и Выход
    exit(0)

input_person = []  # Создаем список где будут хронятся данные для обработки

date_now = date.today()  # Берем сегоднешнию дату
format_day = date_now.strftime("%Y-%m-%d")  # форматируем под нашу задачу
format_year = date_now.strftime("%Y")  # форматируем под нашу задачу Год
f_d = datetime.strptime(format_day, "%Y-%m-%d")  # форматируем под нашу задачу


def cabinet_selection():  # Функция выбора кабинета
    while True:
        cabin = input("Выберете кабинет который хотите забронировать: 1...5\n")  # Принимаем номер кабинета от пользов
        try:
            if int(cabin) in range(1, 6):  # проверяем то что ввел пользователь
                input_person.append(cabin)  # добавляем в список input_person
                break
            else:
                print("error!!! Выберете правельный кабинет! от 1 до 5. СПАСИБО! \n")
        except ValueError:
            print("Вы вводите что-то не то!\n")


def time_and_date_selection():  # Функция которая принимает дату и время бронирования
    while True:
        date_time = input("Введите дату и время когда хотите Забронировать? 07-15 12:00\n")
        try:
            if int(date_time[0:2]) <= 12 and date_time[2:3] == "-" and int(date_time[3:5]) <= 31:  # Проверка данных пол
                if int(date_time[6:8]) <= 24 and date_time[8:9] == ":" and int(date_time[9:11]) <= 59:
                    date_time_format = datetime(month=int(date_time[0:2]), day=int(date_time[3:5]),
                                                year=int(format_year))
                    if date_time_format >= f_d:  # Проверяем что-бы не бронировал в прошлом дне
                        input_person.append(date_time)  # добавляем в список input_person
                        break
                    else:
                        print("Error!!! Вы выбрали день в прошлом \n")
                else:
                    print("Error!!! Выберете правельное время! например - 15:30. СПАСИБО! \n")
            else:
                print("Error!!! Выберете правельное день недели! например - 05-23. СПАСИБО! \n")

        except ValueError:
            print("Вы вводите что-то не то!")


def hours_selection():  # Функция принимает на сколько часов бронируется кабинет
    while True:
        hours = input("продолжительность брони(час-минуты)? н.р 01:20 или 00:40 \n")
        try:
            if int(hours[0:2]) <= 23 and int(hours[3:5]) <= 59 and hours[2:3] == ":":  # Проверяем на валидацию
                input_person.append(hours) # добавляем в список input_person
                break
            else:
                print("НЕВЕРНО!!! Выберете правельную дату! сначала месяц потом день недели \n")
        except ValueError:
            print("Вы вводите что-то не то!")


cabinet_selection()  # Выводим функцию
time_and_date_selection()  # Выводим функцию
hours_selection()  # Выводим функцию

time_start_boking = timedelta(hours=int(input_person[1][6:8]), minutes=int(input_person[1][9::])) # строку в объект даты
time_end_booking = time_start_boking + timedelta(hours=int(input_person[2][0:2]), minutes=int(input_person[2][3::])) - \
                   timedelta(minutes=1)
cabin_namber = f"cabin_%s" % (input_person[0])  # форматируем под нашу задачу
dat = input_person[1][0:5]  # из  списка берем время начало бронирования


def search_in_bd_booking():
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT * FROM `{cabin_namber}` WHERE `date` LIKE '%{dat}%' AND `time` >= '{time_start_boking}'"
                       f" AND `hour` <= '{time_end_booking}' OR `hour` >='{time_start_boking}' AND `time` <= "
                       f"'{time_end_booking}'")
        rows = cursor.fetchall()
        if len(rows) >= 1:
            for row in sorted(rows, key=lambda x: x['time']):
                print("На это время", row.get('full_name'), "\nзабронировал",
                      input_person[0], 'кабинет. C', row.get('time'), "до", row.get('hour'))
        else:
            print('C', time_start_boking, 'до', time_end_booking, 'свободен', cabin_namber[6], 'кабинет')



search_in_bd_booking()
