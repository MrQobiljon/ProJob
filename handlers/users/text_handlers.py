from telebot.types import Message, ReplyKeyboardRemove

from data.loader import bot, db
from keyboards.inline import send_type_work



@bot.message_handler(func=lambda message: message.text == '🏘Bosh sahifa')
def reaction_to_default_main_menu(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    bot.send_message(chat_id, "Bosh sahifa!", reply_markup=ReplyKeyboardRemove())
    directions_list = db.select_value_in_directions()
    bot.send_message(chat_id, "<b>Qaysi yo'nalishda ish bermoqchisiz?</b>", reply_markup=send_type_work(directions_list, from_user_id))



@bot.message_handler(content_types=['contact'])
def reaction_to_contact(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    phone_number = message.contact.phone_number
    db.update_phone_number(phone_number, chat_id)
    bot.send_message(chat_id, "Telefon raqam qabul qilindi😊", reply_markup=ReplyKeyboardRemove())
    directions_list = db.select_value_in_directions()
    bot.send_message(chat_id, "<b>Qaysi yo'nalishda ish bermoqchisiz?</b>", reply_markup=send_type_work(directions_list, from_user_id))