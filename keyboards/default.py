from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def send_phone_number():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn = KeyboardButton('Kontaktni ulashish', request_contact=True)
    markup.add(btn)
    return markup


def default_main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn = KeyboardButton('🏘Bosh sahifa')
    markup.add(btn)
    return markup


def admin_commands_buttons():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    command1 = KeyboardButton('/add_direction')
    command2 = KeyboardButton('/delete_direction')
    command3 = KeyboardButton('/add_admin')
    command4 = KeyboardButton('/delete_admin')
    main_menu = KeyboardButton('🏘Bosh sahifa')
    markup.add(command1, command2, command3, command4)
    markup.row(main_menu)
    return markup


def send_all_admins(admin_list):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    for admin in admin_list:
        btn = KeyboardButton(admin[0])
        markup.add(btn)
    btn2 = KeyboardButton('🏘Bosh sahifa')
    back = KeyboardButton("⬅️Ortga")
    markup.add(btn2, back)
    return markup


def send_back():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    back = KeyboardButton("⬅️Ortga")
    markup.add(back)
    return markup