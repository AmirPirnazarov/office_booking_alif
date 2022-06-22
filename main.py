from datetime import *
import pymysql.cursors
import re
import smtplib
from email.mime.text import MIMEText
from twilio.rest import Client
try:  # Проверяем методом исключения подключение к БД MySQL
    connection = pymysql.connect(host='localhost',  # Имя хоста
                                 user='root',  # Имя пользоватеся
                                 db='booking',  # Название Базы данных
                                 charset='utf8mb4',  # Кодировка
                                 cursorclass=pymysql.cursors.DictCursor)  # Выбираем класс для подключ
    print("connect on BD successful!!")  # Выводим что успешко подключился
except pymysql.err.OperationalError:
    print("not connection on BD!!")  # Если не подключенно то выводит следующее сообщение! и Выход
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
                input_person.append(hours)  # добавляем в список input_person
                break
            else:
                print("НЕВЕРНО!!! Выберете правельную дату! сначала месяц потом день недели \n")
        except ValueError:
            print("Вы вводите что-то не то!")


cabinet_selection()  # Выводим функцию
time_and_date_selection()  # Выводим функцию
hours_selection()  # Выводим функцию

time_start_boking = timedelta(hours=int(input_person[1][6:8]), minutes=int(input_person[1][9::]))  # строку в объект дат
time_end_booking = time_start_boking + timedelta(hours=int(input_person[2][0:2]), minutes=int(input_person[2][3::])) - \
                   timedelta(minutes=1)
cabin_namber = f"cabin_%s" % (input_person[0])  # форматируем под нашу задачу
dat = input_person[1][0:5]  # из  списка берем время начало бронирования


def search_in_bd_booking():
    with connection.cursor() as cursor:  # подключение к бд
        cursor.execute(f"SELECT * FROM `{cabin_namber}` WHERE `date` LIKE '%{dat}%' AND `time` >= '{time_start_boking}'"
                       f" AND `hour` <= '{time_end_booking}' OR `hour` >='{time_start_boking}' AND `time` <= "
                       f"'{time_end_booking}'")  # Запрос к бд поиск пересечений времени
        rows = cursor.fetchall()
        if len(rows) >= 1:  # если найдет в этот день то
            for row in sorted(rows, key=lambda x: x['time']):  # через цыкл сортируем и выводим сортированный список
                print("На это время", row.get('full_name'), "\nзабронировал",
                        input_person[0], 'кабинет. C', row.get('time'), "до", row.get('hour'))
            search_in_bd_all_booking()
        else:
            print('C', time_start_boking, 'до', time_end_booking, 'свободен', cabin_namber[6], 'кабинет')
            booking = input("Забронировать? Y/n\n")  # Если в этот день нет забронированных спрашивает
            if booking.lower() == 'y':  # проверяет что ввел пользователь и прееводит в строчный текст
                insert_in_bd_booking()
            else:
                print('Всего хорошего!')


def input_email():
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'  # Регулярные вырожения для проверки валидации
    password = "****************"  # Пароль от почты
    email_sendler = "pirnazarova988@gmail.com"  # почта с которого будет отправляться сообщение
    while True:  # бесконечный цыкл
        email = input("Введите свой email\n")
        try:
            if re.fullmatch(regex, email):  # Проверка на валидацию
                input_person.append(email)  # Доб в список
                smtp_server = smtplib.SMTP("smtp.gmail.com", 587)  # Создание обьекта smtp_server
                smtp_server.starttls()  # Шифрование сообщений
                smtp_server.login(email_sendler, password)  # вход на почту
                msg = MIMEText(
                    f"{str(input_person[0])}кабинет. С {time_start_boking} до {time_end_booking}. Занят "
                    f"{str(input_person[3])}")
                msg["Subject"] = "Бронирование кабинетов"  # текст сообщения
                smtp_server.sendmail(email_sendler, email, msg.as_string())  # отправляем сообщение
                smtp_server.quit()  # Выход
                input_phone()
                break
            else:
                print("НЕВЕРНО!!! Вы ввели не правельный email \n")
        except ValueError:
            print("Вы вводите что-то не то!")


def input_phone():
    regex_phone = r'^[+]?[0-9]{3}?[0-9]{9}$'  # Регулярные вырожения для проверки валидации
    cabin_namber = f"cabin_%s" % (input_person[0])
    while True:
        phone = input("Введите свой номер телефона н.р.(937777777)\n")  # принимает номер телефона от пользователя
        phone_full = '+992' + phone  # доб код страны автомат
        try:
            if re.fullmatch(regex_phone, phone_full):  # проверка на валидацию
                input_person.append(phone)  # Доб в список
                client = Client("AC0de*8a37*2b2d4f0666619493238****", "263e2f1e76b10ff1aebcddc8b4ff2d38")  # Вход
                client.messages.create(to=phone_full,  # отправляем на номер тел
                                       from_="+1*80*75155*",  # мой номер тел
                                       body=f"{str(input_person[0])} кабинет. С {time_start_boking} до "
                                            f"{time_end_booking}. Занят {str(input_person[3])}")  # текст сообщения
                with connection.cursor() as cursor:  # подкл к БД
                    cursor.execute(f"INSERT INTO `{cabin_namber}`(`date`,`time`,`hour`,`full_name`,`email`,`phone`) "
                                   f"VALUES('{format_year}-{dat}', '{time_start_boking}', '{time_end_booking}', "
                                   f"'{input_person[3]}', '{input_person[4]}', '{input_person[5]}')")  # Доб В БД
                    print("Спасибо вы забронировали!")
                connection.commit()
                break
            else:
                print("НЕВЕРНО!!! Вы ввели не правельный email \n")
        except ValueError:
            print("Вы вводите что-то не то!")


def insert_in_bd_booking():
    cabin_namber = f"cabin_%s" % (input_person[0])
    full_name = input("На кого забронировать? н.р. Амир Пирназаров\n") # Принимает имя пользов
    input_person.append(full_name) # Доб в список
    message = input("Отправить уведомление? Y/n\n") # Спрашиваем отправить уведомление
    if message.lower() == 'y':
        input_email()
    elif message.lower() == 'n':
        with connection.cursor() as cursor: # Подк к БД
            cursor.execute(f"INSERT INTO `{cabin_namber}`(`date`,`time`,`hour`,`full_name`) "
                           f"VALUES('{format_year}-{dat}', '{time_start_boking}', '{time_end_booking}',"
                           f" '{input_person[3]}')") # Доб в БД
            print("Спасибо вы забронировали!")
        connection.commit()
    else:
        print("Я не понимаю вас!")
        insert_in_bd_booking()


def search_in_bd_all_booking():
    with connection.cursor() as cursor: # Подкл к БД
        while True:
            for x in range(1, 5):  # Цыкл из 5 кабинетов проверяем если забронированно то искать в другом кабинете
                cabin_nambers = f"cabin_%s" % (int(input_person[0]) + x)  # Меняем кабинет
                cursor.execute(f"SELECT * FROM `{cabin_nambers}` WHERE `date` LIKE '%{dat}%' AND `time` >= "
                               f"'{time_start_boking}'"
                               f" AND `hour` <= '{time_end_booking}' OR `hour` >='{time_start_boking}' AND `time` <= "
                               f"'{time_end_booking}'") # Поиск в БД
                rows = cursor.fetchall()
                if len(rows) < 1:
                    print('C', time_start_boking, 'до', time_end_booking, 'свободен', cabin_nambers[6], 'кабинет')
                    booking = input("Забронировать? Y/n\n")  # Спрашиваем у пользов
                    if booking.lower() == 'y':
                        input_person[0] = cabin_nambers[6]  # Меняем значение кабинете в списке 
                        insert_in_bd_booking()
                    else:
                        break
                    break
            break


search_in_bd_booking()
