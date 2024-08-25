import classes
import configparser


config = configparser.ConfigParser()
print("Welcome to saloon!")
oper = input(
    "If you are here for the first time type 'register',else press 'Enter': "
).lower()

"""Регистрация нового пользователя.
По окончанию регистрации логин и пароль записываются в файл my_config.ini."""

while oper == "register":
    try:
        u_name = input("Write your username here: ")
        config.read("my_config.ini")
        while u_name in config["Customer"]:
            u_name = input("This username already exists! Choose a different one: ")
        u_password = input("Set your password: ")
        new_user = classes.User(u_name, u_password)
        config.set("Customer", u_name, u_password)

        with open("my_config.ini", "w") as configfile:
            config.write(configfile)
            print("You've been registered!")

    except Exception as e:
        print(e)
    oper = input("To continue registration type 'register',else press 'Enter': ")


"""Вход в систему через логин-пароль."""
'''Для админа.'''

user_name = input("Please, enter your username: ")
if user_name == "admin":
    config.read("my_config.ini")
    admin_password = config.get("Admin", "password")
    password = input("Enter your password: ")
    if password != admin_password:
        count = 0
        while count < 4:
            count += 1
            password = input("Wrong! Try again: ")
        print("You have failed 5 attempts! You are blocked!")
        classes.logging.critical("5 attempts failed! Admin is blocked!")

    else:
        print("Welcome!")

else:
    '''Вход через логин/пароль для клиента.'''

    config.read("my_config.ini")
    while user_name not in config["Customer"]:
        user_name = input("Not found! Please, try again! Username: ")

    password = input("Enter your password: ")
    while password != config.get("Customer", user_name):
        password = input("Not matching! Try again! Password: ")

"""Выводим меню пользователя. Создаем или изменяем запись."""

classes.user_menu()
operation = input("Choose from the menu: ")

while operation != "0":
    '''Создаем запись через класс Client.'''

    if operation == "1":
        customer_info = {}
        while customer_info == {}:
            try:
                name = input("To make appointment, please, enter your name: ").strip()
                mobile = input("Enter your phone number: ").strip()
                service = (
                    input("Choose the option available (hair, nails, lashes): ")
                    .lower()
                    .strip()
                )
                customer_info = classes.Client(mobile, name, service)
            except Exception as e:
                print(e)

        print("Your appointment is done!")
        classes.Client.show_all_appointments()
        classes.user_menu()
        operation = input("Choose from the menu: ")
    elif operation == "2":
        '''Изменяем запись по номеру теелфона.'''

        mobile = input("To change appointment enter your phone number: ").strip()
        if mobile not in classes.Client.list_of_clients:
            mobile = input("This number is wrong! Try again: ")
        else:    
          changed_service = (
            input("Choose the option available (hair, nails, lashes): ").lower().strip()
         )
          customer_info.change_service(mobile, changed_service)
          customer_info.show_appointment(mobile)
          classes.user_menu()
          operation = input("Choose from the menu: ")
    elif operation == "3":
        '''Отменяем запись по номеру телефона.'''

        mobile = input("To cancel appointment enter your phone number: ").strip()
        if mobile not in classes.Client.list_of_clients:
            mobile = input("This number is wrong! Try again: ")
        else:    
          customer_info.delete_appointment(mobile)
          print("Your appointment is cancelled! You can make a new one.")
          classes.user_menu()
          operation = input("Choose from the menu: ")
    elif operation == "4":
        '''Доступ к функциям админа. Запрашиваем пароль админа.'''

        config.read("my_config.ini")
        admin_password = config.get("Admin", "password") #  Сверка пароля с файлом my_config.ini
        password = input("Enter admin password: ")
        if password != admin_password:
            print("Access denied!")
            operation = input("Choose from the menu: ")
        else:
            classes.admin_menu()
            oper = input("Choose from the menu: ")
            if oper == "1":
                classes.write_to_Json()
            elif oper == "2":
                client_phone = input("Please, enter the phone number of the client: ")
                classes.del_from_sqlite(client_phone) 
                print("The appointment is cancelled!")   
            else:
                print("Wrong operation!")
                classes.admin_menu()
                oper = input("Choose from the menu: ")
        classes.user_menu()
        operation = input("Choose from the menu: ")

    else:
        print("Wrong operation!")
        classes.user_menu()
        operation = input("Choose from the menu: ")

else:
    print("Thank you! Good bye!")
