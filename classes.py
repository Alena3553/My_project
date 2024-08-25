import sqlite3
import json
import logging


"""Создаём файл customers.log."""

logging.basicConfig(
    filename="customers.log",
    level=logging.DEBUG,
    format="%(asctime)s:%(levelname)s:%(message)s",
)


class User_name_Error(Exception):
    """Класс обработки ошибки логина."""

    def __init__(self, message):
        self.message = message
        logging.info("Username error!")


class Password_error(Exception):
    """Класс обработки ошибки пароля."""

    def __init__(self, message):
        self.message = message
        message = "Password should be not less than 7 symbols!"
        logging.info("Password error!")


class Name_error(Exception):
    """Класс обработки ошибки имени клиента."""

    def __init__(self, message):
        self.message = message
        logging.info("Name error!")


class Service_error(Exception):
    """Класс обработки ошибки услуги."""

    def __init__(self, message):
        self.message = message
        logging.info("Service error!")


class Phone_number_error(Exception):
    """Класс обработки ошибки номера телефона."""

    def __init__(self, message):
        self.message = message
        logging.info("Phone number error!")


class User:
    """Класс для регистрации пользователя в приложении."""

    list_of_users = {}

    def __init__(self, user_name, password):
        self.u_name = user_name
        self.password = password
        if len(user_name) < 5:
            raise User_name_Error(
                "Too short! Username should be not less than 5 symbols!"
            )
        if len(password) < 7:
            raise Password_error("Password should be not less than 7 symbols!")
        User.list_of_users[user_name] = password


class Client:
    """Класс для создания и управления записью."""

    list_of_service = ["hair", "nails", "lashes"]
    list_of_clients = {}

    def __init__(self, phone, name, service):
        self.name = name
        self.phone = phone
        self.service = service
        if len(name) < 2:
            raise Name_error("Please, write the correct name!")
        elif self.service not in Client.list_of_service:
            raise Service_error("Choose the option from the list!")
        elif len(phone) < 7:
            raise Phone_number_error("Phone number should be not less than 7 digits!")

        Client.list_of_clients[phone] = [name, service]
        """Отправляем информацию о записи в БД."""

        conn = sqlite3.connect("customers.db")
        c = conn.cursor()
        # создаем таблицу.
        c.execute(
            """CREATE TABLE IF NOT EXISTS customers(
            phone TEXT NOT NULL,
            name TEXT NOT NULL,
            service TEXT NOT NULL
            );"""
        )
        # ввод данных.
        c.execute(
            "INSERT INTO customers(phone, name, service) VALUES (?,?,?)",
            (phone, name, service),
        )
        # фиксируем изменения.
        conn.commit()
        # закрываем соединение.
        conn.close()

    def show_appointment(self, phone):
        self.phone = phone
        print(f"Your appointment: {Client.list_of_clients[phone]}")

    def change_service(self, phone, service):
        self.phone = phone
        self.service = service
        Client.list_of_clients[phone] = self.name, service
        conn = sqlite3.connect("customers.db")
        c = conn.cursor()
        c.execute("UPDATE customers SET service = ? WHERE phone = ?", (service, phone))
        conn.commit()
        conn.close()

    def delete_appointment(self, phone):
        self.phone = phone
        Client.list_of_clients.pop(phone)
        conn = sqlite3.connect("customers.db")
        c = conn.cursor()
        c.execute("DELETE FROM customers WHERE phone = ?", (phone,))
        conn.commit()
        conn.close()

    def show_all_appointments():
        if len(Client.list_of_clients) != 0:
            for key in Client.list_of_clients.keys():
                print(key, Client.list_of_clients[key])


def user_menu():
    print(
        """
          1 - Make an appointment
          2 - Change the existing appointment
          3 - Cancel appointment
          4 - Admin options
          0 - Leave the program 
          """
    )


def admin_menu():
    print(
        """
          1 - Create Json document
          2 - Delete appointment from DB

           """
    )


def write_to_Json():
    # Подключение к базе данных
    conn = sqlite3.connect("customers.db")
    cursor = conn.cursor()

    # Выполнение запроса
    cursor.execute("SELECT * FROM customers")
    rows = cursor.fetchall()
    # Запись данных
    data = rows
    with open("data.json", "w") as file:
        json.dump(data, file, indent = 1)
    conn.close()    


'''Функция удаляет запись из БД по номеру телефона.'''

def del_from_sqlite(phone):
    conn = sqlite3.connect("customers.db")
    c = conn.cursor()
    c.execute("DELETE FROM customers WHERE phone = ?", (phone,))
    conn.commit()
    conn.close()
