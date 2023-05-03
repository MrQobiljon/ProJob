from telebot.types import Message, ReplyKeyboardRemove

from data.loader import bot, db
from keyboards.inline import start_markup, send_type_work
from keyboards.default import send_phone_number



@bot.message_handler(commands=['start'], chat_types=['private', 'group', 'supergroup'])
def welcome(message: Message):
    from_user_id = message.from_user.id
    chat_id = message.chat.id

    db.insert_telegram_id_users(from_user_id)
    status = ['creator', 'administrator', 'member']
    if bot.get_chat_member(chat_id='-1001844564266', user_id=from_user_id).status not in status:
        bot.send_message(chat_id, text=f"Assalomu alaykum {message.from_user.full_name}!\n"
                                       f"Botdan foydalanish uchun kanalga obuna bo'ling", reply_markup=start_markup())
    else:
        try:
            check = db.select_phone_number(from_user_id)
            if None in check:
                bot.send_message(chat_id,
                                 f"Assalomu alaykum {message.from_user.full_name} <b>ProJob</b> botiga xush kelibsiz! "
                                 f"Tugmani bosib tel nomeringizni yuboring😊", reply_markup=send_phone_number())
            else:
                directions_list = db.select_value_in_directions()
                bot.send_message(chat_id, "<b>Assalomu alaykum!</b>", reply_markup=ReplyKeyboardRemove())
                bot.send_message(chat_id, "<b>Qaysi yo'nalishda ish bermoqchisiz?</b>", reply_markup=send_type_work(directions_list, from_user_id))
        except:
            pass
























# def check(cell):
#     status = ['creator', 'administrator', 'member']
#     for i in status:
#         if i == bot.get_chat_member(chat_id='-1001980233151', user_id=cell.message.chat.id).status:
#             bot.send_message(chat_id=cell.message.chat.id, text="Kanalga ulanganiz uchun rahmat")
#             break
#
#     else:
#         bot.send_message(cell.message.chat.id, "Kanalta a'zo bo'ling", reply_markup=start_markup())