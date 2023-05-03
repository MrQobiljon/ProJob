from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import ADMINS

def start_markup():
    markup = InlineKeyboardMarkup()
    btn = InlineKeyboardButton(text="Kanal", url='https://t.me/projobuz')
    markup.add(btn)
    return markup



# def send_direction():
#     markup = InlineKeyboardMarkup()
#     btn1 = InlineKeyboardButton("👨‍💼Ish beruvchi", callback_data='employer')
#     btn2 = InlineKeyboardButton("👨‍💻Ish oluvchi", callback_data='freelancer')
#     markup.add(btn1, btn2)
#     return markup



def send_type_work(directions_list, chat_id):
    markup = InlineKeyboardMarkup(row_width=2)
    for direction in directions_list:
        btn = InlineKeyboardButton(direction[0], callback_data=f"select|{direction[0]}")
        markup.add(btn)
    btn2 = InlineKeyboardButton("💼Mening buyurtmalarim", callback_data="my_orders")
    btn3 = InlineKeyboardButton("⚙️Sozlamalar", callback_data="settings")
    btn4 = InlineKeyboardButton("☎️Operator bilan bog'lanish", callback_data="operator")
    markup.row(btn2, btn3)
    markup.add(btn4)

    btn5 = InlineKeyboardButton("📋Admin buruqlari", callback_data="admin_commands")
    if chat_id in ADMINS:
        markup.add(btn5)
    return markup


def confirmation_button():
    markup = InlineKeyboardMarkup(row_width=2)
    btn1 = InlineKeyboardButton("Xa", callback_data="yes")
    btn2 = InlineKeyboardButton("Yo'q", callback_data="no")
    markup.add(btn1, btn2)
    return markup


def send_all_directions_to_delete(directions_list):
    markup = InlineKeyboardMarkup()
    for direction in directions_list:
        btn = InlineKeyboardButton(direction[0], callback_data=f"delete|{direction[0]}")
        markup.add(btn)
    main_menu = InlineKeyboardButton("🏘Bosh sahifa", callback_data="main_menu")
    markup.add(main_menu)
    return markup


def settings_buttons():
    markup = InlineKeyboardMarkup(row_width=2)
    btn1 = InlineKeyboardButton("🔄Ismni o'zgartirish", callback_data="update_name")
    btn2 = InlineKeyboardButton("📞Telefon nomerni o'zgartirish", callback_data="update_phone")
    main_menu = InlineKeyboardButton("🏘Bosh sahifa", callback_data="main_menu")
    markup.add(btn1, btn2, main_menu)
    return markup