# from telebot.types import Message
#
# from data.loader import bot, db
# from keyboards.default import admin_commands_buttons
#
#
# @bot.message_handler(func=lambda message: message.text == "Admin buyruqlari")
# def reaction_to_bosh_sahifa(message: Message):
#     chat_id = message.chat.id
#     bot.send_message(chat_id, "Kerakli buruqni tanlang!", reply_markup=admin_commands_buttons())