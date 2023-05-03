from telebot.types import Message, ReplyKeyboardRemove

from data.loader import bot, db
from keyboards.default import admin_commands_buttons, send_all_admins
from keyboards.inline import send_all_directions_to_delete, send_type_work
from config import ADMINS


@bot.message_handler(commands=['add_direction'])
def reaction_to_direction(message: Message):
    chat_id = message.chat.id
    from_user_id = message.chat.id
    if from_user_id in ADMINS:
        msg = bot.send_message(chat_id, "Yo'nalishni kiriting")
        bot.register_next_step_handler(msg, save_direction)

def save_direction(message: Message):
    chat_id = message.chat.id
    direction = message.text
    db.insert_value_to_directions(direction)
    bot.send_message(chat_id, "Yo'nalish saqlandi!", reply_markup=admin_commands_buttons())


@bot.message_handler(commands=['delete_direction'])
def reaction_to_direction(message: Message):
    chat_id = message.chat.id
    from_user_id = message.chat.id
    if from_user_id in ADMINS:
        bot.send_message(chat_id, "O'chirmoqchi bo'lgan yo'nalishingizni tanlang!", reply_markup=ReplyKeyboardRemove())
        directions_list = db.select_value_in_directions()
        bot.send_message(chat_id, "Yo'nalishlar", reply_markup=send_all_directions_to_delete(directions_list))


@bot.message_handler(commands=['send'])
def reaction_to_send(message: Message):
    from_user_id = message.from_user.id
    chat_id = message.chat.id
    try:
        if from_user_id in ADMINS:
            bot.copy_message('-1001844564266', chat_id, message.reply_to_message.message_id)
            bot.send_message(chat_id, "<b>Bu e'lon kanalga joylandi!</b>", reply_to_message_id=message.reply_to_message.message_id)
    except:
        pass



admin_data = {}
@bot.message_handler(commands=['add_admin'])
def reaction_to_add_admin(message: Message):
    from_user_id = message.from_user.id
    chat_id = message.chat.id
    if from_user_id in ADMINS and not message.from_user.is_bot:
        admin_data[from_user_id] = {}
        msg = bot.send_message(chat_id, "<b>Yangi adminni telegram idsini kiriting!</b>", reply_markup=ReplyKeyboardRemove())
        bot.register_next_step_handler(msg, save_telegram_admin)
    else:
        bot.send_message(chat_id, "<b>Sizda yangi admin qo'shishga huquq yo'q!</b>", reply_markup=admin_commands_buttons())

def save_telegram_admin(message: Message):
    from_user_id = message.from_user.id
    chat_id = message.chat.id
    try:
        admin_id = int(message.text)
        admin_data[from_user_id]['admin_id'] = admin_id
        msg = bot.send_message(chat_id, "<b>Yangi admin ismini kiriting!</b>")
        bot.register_next_step_handler(msg, save_name_admin)
    except:
        bot.send_message(chat_id, "<b>Nimadir xato ketdi!</b>", reply_markup=admin_commands_buttons())

def save_name_admin(message: Message):
    from_user_id = message.from_user.id
    chat_id = message.chat.id
    try:
        admin_name = message.text
        admin_id = admin_data[from_user_id]['admin_id']
        db.insert_admin(admin_id, admin_name)
        bot.send_message(chat_id, "<b>Yangi admin qo'shildi!</b>", reply_markup=admin_commands_buttons())
    except:
        bot.send_message(chat_id, "<b>Nimadir xato ketdi!</b>", reply_markup=admin_commands_buttons())



@bot.message_handler(commands=['delete_admin'])
def reaction_to_add_admin(message: Message):
    from_user_id = message.from_user.id
    chat_id = message.chat.id
    if from_user_id in ADMINS and not message.from_user.is_bot:
        admin_list = db.select_admins()
        msg = bot.send_message(chat_id, "<b>O'chirish uchun admini tanlang!</b>", reply_markup=send_all_admins(admin_list))
        bot.register_next_step_handler(msg, commit_delete_admin)

def commit_delete_admin(message: Message):
    from_user_id = message.from_user.id
    chat_id = message.chat.id
    admin_name = message.text
    try:
        if message.text == "🏘Bosh sahifa":
            bot.send_message(chat_id, "Bosh sahifa!", reply_markup=ReplyKeyboardRemove())
            directions_list = db.select_value_in_directions()
            bot.send_message(chat_id, "<b>Qaysi yo'nalishda ish bermoqchisiz?</b>", reply_markup=send_type_work(directions_list, from_user_id))
        elif message.text == "⬅️Ortga":
            bot.send_message(chat_id, "<b>Admin buyruqlari!</b>", reply_markup=admin_commands_buttons())
        else:
            db.delete_admin(admin_name)
            bot.send_message(chat_id, "<b>Admin o'chirildi!</b>", reply_markup=admin_commands_buttons())
    except:
        bot.send_message(chat_id, "<b>Nimadir xato ketdi!</b>", reply_markup=admin_commands_buttons())