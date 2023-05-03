from telebot.types import Message, CallbackQuery
from data.loader import bot, db
from keyboards.default import admin_commands_buttons
from keyboards.inline import send_type_work


@bot.callback_query_handler(func=lambda call: "delete" in call.data)
def reaction_to_delete_direction(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    direction = call.data.split("|")[1]
    print(direction)
    bot.delete_message(chat_id, call.message.message_id)
    try:
        db.delete_value_in_directions(direction)
        bot.send_message(chat_id, "Yo'nalish o'chirildi!", reply_markup=admin_commands_buttons())
    except:
        bot.send_message(chat_id, "<b>Nimadir xato ketdi!</b>")
        directions_list = db.select_value_in_directions()
        bot.send_message(chat_id, "<b>Qaysi yo'nalishda ish bermoqchisiz?</b>", reply_markup=send_type_work(directions_list, from_user_id))