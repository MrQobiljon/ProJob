from telebot.types import CallbackQuery, Message, ReplyKeyboardRemove

from data.loader import bot, db
from keyboards.inline import send_type_work, confirmation_button, settings_buttons
from keyboards.default import default_main_menu, admin_commands_buttons, send_back, send_phone_number
from config import ADMINS

WORK_TYPE = ['site', 'bot', 'design']


# -----------------------------------------------------------------------------------------------------------------


@bot.callback_query_handler(func=lambda call: call.data == 'main_menu')
def reaction_to_main_menu(call: CallbackQuery):
    from_user_id = call.from_user.id
    chat_id = call.message.chat.id
    bot.delete_message(chat_id, call.message.message_id)
    directions_list = db.select_value_in_directions()
    bot.send_message(chat_id, "<b>Qaysi yo'nalishda ish bermoqchisiz?</b>", reply_markup=send_type_work(directions_list, from_user_id))


# -----------------------------------------------------------------------------------------------------------------

data = {}
@bot.callback_query_handler(func=lambda call: 'select' in call.data)
def reaction_to_call_freelancer(call: CallbackQuery):
    from_user_id = call.from_user.id
    chat_id = call.message.chat.id
    data[chat_id] = {}
    bot.delete_message(chat_id, call.message.message_id)
    direction = call.data.split('|')[1]
    print(direction)
    data[chat_id]['work_type'] = direction

    msg = bot.send_message(chat_id, f"<b>Loyixa nomini kiriting</b>")
    bot.register_next_step_handler(msg, get_title_from_employer)


def get_title_from_employer(message: Message):
    from_user_id = message.from_user.id
    chat_id = message.chat.id
    title = message.text
    data[chat_id]['title'] = title
    msg = bot.send_message(chat_id, "<b>Loyixa qanday bo'lishi haqida ma'lumot bering</b>")
    bot.register_next_step_handler(msg, get_text_from_employer)


def get_text_from_employer(message: Message):
    chat_id = message.chat.id
    content = message.text
    data[chat_id]['content'] = content
    msg = bot.send_message(chat_id, "<b>Loyixani tayyorlashlari uchun qancha <i>so'm</i> to'laysiz?</b>")
    bot.register_next_step_handler(msg, get_price_from_employer)


def get_price_from_employer(message: Message):
    chat_id = message.chat.id
    try:
        price = int(message.text)
        data[chat_id]['price'] = price

        title = data[chat_id]['title']
        content = data[chat_id]['content']
        price = data[chat_id]['price']

        announcement = f'''<b><i>Sizning buyurtmangiz</i></b>
<b>{title}</b>

{content}

<b>Narxi: <i>{price}</i> so'm</b>'''

        bot.send_message(chat_id, announcement)
        bot.send_message(chat_id, "Xabarni jo'natishni xoxlaysizmi?", reply_markup=confirmation_button())
    except:
        msg = bot.send_message(chat_id, "<b>Narxni raqam bilan kiriting❗️❗️❗️\nLoyixani tayyorlashlari uchun qancha <i>so'm</i> to'laysiz?</b>")
        bot.register_next_step_handler(msg, get_price_from_employer)


# -----------------------------------------------------------------------------------------------------------------

@bot.callback_query_handler(func=lambda call: call.data == 'yes')
def reaction_to_confirmation_yes(call: CallbackQuery):
    from_user_id = call.from_user.id
    chat_id = call.message.chat.id
    try:
        title = data[chat_id]['title']
        content = data[chat_id]['content']
        price = data[chat_id]['price']
        work_type = data[chat_id]['work_type']

        db.insert_work(from_user_id, title, content, price, work_type)
        bot.delete_message(chat_id, call.message.message_id)

        announcement = f'''<b><i>{work_type}</i></b>
        
<b>{title}</b>
    
{content}
    
<b>Narxi: <i>{price}</i> so'm</b>'''

        bot.send_message(chat_id, announcement)
        bot.send_message(chat_id, """Ma'lumotlar adminga yuborildi!
Sizning e'loningiz 3 soat ichida tekshirilib, kanalga joylanadi
Siz o'z e'loningizni quyidagi <a href="https://t.me/projobuz">ProJob</a> kalanaldan ko'rishingiz mumkin""",
                         reply_markup=default_main_menu())

        user_phone_number = db.select_phone_number(from_user_id)[0]
        if from_user_id in ADMINS:

            announcement = f'''#buyurtma
<b><i>{work_type}</i></b>

<b>{title}</b>

{content}

<b>Narxi: <i>{price}</i> so'm</b>'''

            try:
                user_info = f"\n\n" \
                                f"<b>Buyurtmachi:</b> {call.from_user.full_name}\n" \
                                f"<b>Username:</b> @{call.from_user.username}\n" \
                            f"Phone: {user_phone_number}"
                bot.send_message(-1001773139084, announcement)
                bot.send_message(-1001773139084, user_info)
            except:
                pass
    except:
        pass


@bot.callback_query_handler(func=lambda call: call.data == 'no')
def reaction_to_confirmation_no(call: CallbackQuery):
    from_user_id = call.from_user.id
    chat_id = call.message.chat.id
    bot.delete_message(chat_id, call.message.message_id - 1)
    bot.delete_message(chat_id, call.message.message_id)
    directions_list = db.select_value_in_directions()
    bot.send_message(chat_id, "<b>Qaysi yo'nalishda ish bermoqchisiz?</b>", reply_markup=send_type_work(directions_list, from_user_id))



# -----------------------------------------------------------------------------------------------------------------


@bot.callback_query_handler(func=lambda call: call.data == 'admin_commands')
def reaction_to_confirmation_yes(call: CallbackQuery):
    chat_id = call.message.chat.id
    bot.delete_message(chat_id, call.message.message_id)
    bot.send_message(chat_id, "Admin buyruqlari!", reply_markup=admin_commands_buttons())


@bot.callback_query_handler(func=lambda call: call.data == 'my_orders')
def reaction_to_my_commands(call: CallbackQuery):
    from_user_id = call.from_user.id
    chat_id = call.message.chat.id
    bot.delete_message(chat_id, message_id=call.message.message_id)

    works = db.select_works_users_by_telegram_id(from_user_id)
    for work in works:
        work_info = f"""{work[4]}
<b>Mavzu</b>: {work[1]}
<b>Izohi</b>: {work[2]}
<b>Narxi</b>: {work[3]}"""
        bot.send_message(chat_id, work_info)

    count_works = len(db.select_works_users_by_telegram_id(from_user_id))

    bot.send_message(chat_id, f"<b>Sizda jami: <i>{count_works}</i> ta buyurtma bor!</b>", reply_markup=default_main_menu())



@bot.callback_query_handler(func=lambda call: call.data == 'settings')
def reaction_to_settings(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    bot.delete_message(chat_id, call.message.message_id)
    bot.send_message(chat_id, "<b>Ma'lumotlarnigizni o'zgartiring!</b>", reply_markup=settings_buttons())



@bot.callback_query_handler(func=lambda call: call.data == 'operator')
def reaction_to_settings(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    bot.delete_message(chat_id, call.message.message_id)
    directions_list = db.select_value_in_directions()
    bot.send_message(chat_id, "Operator tel nomeri!", reply_markup=send_type_work(directions_list, from_user_id))


# -----------------------------------------------------------------------------------------------------------------

@bot.callback_query_handler(func=lambda call: call.data == 'update_name')
def reaction_to_settings(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    bot.delete_message(chat_id, call.message.message_id)
    msg = bot.send_message(chat_id, "<b>To'liq ismingizni kiriting!</b>", reply_markup=send_back())
    bot.register_next_step_handler(msg, get_name_for_update)

def get_name_for_update(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    name = message.text
    try:
        if message.text == "⬅️Ortga":
            bot.send_message(chat_id, "<b>Sozlamalar</b>", reply_markup=ReplyKeyboardRemove())
        else:
            db.update_full_name(name, from_user_id)
            bot.send_message(chat_id, "<b>Ism o'zgartirlidi!</b>", reply_markup=ReplyKeyboardRemove())
        bot.send_message(chat_id, "<b>Ma'lumotlarnigizni o'zgartiring!</b>", reply_markup=settings_buttons())
    except:
        bot.send_message(chat_id, "<b>Nimadir hato ketdi!</b>", reply_markup=ReplyKeyboardRemove())
        bot.send_message(chat_id, "<b>Ma'lumotlarnigizni o'zgartiring!</b>", reply_markup=settings_buttons())


@bot.callback_query_handler(func=lambda call: call.data == 'update_phone')
def reaction_to_settings(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    bot.delete_message(chat_id, call.message.message_id)
    msg = bot.send_message(chat_id, f"<b>Tugmani bosib tel nomeringizni yuboring😊</b>", reply_markup=send_phone_number())
    bot.register_next_step_handler(msg, get_contact_for_update)

def get_contact_for_update(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    try:
        phone_number = message.contact.phone_number
        db.update_phone_number(phone_number, from_user_id)
        bot.send_message(chat_id, "<b>Telefon nomer o'zgartirildi!</b>", reply_markup=ReplyKeyboardRemove())
        bot.send_message(chat_id, "<b>Ma'lumotlarnigizni o'zgartiring!</b>", reply_markup=settings_buttons())
    except:
        bot.send_message(chat_id, "<b>Nimadir hato ketdi!</b>", reply_markup=ReplyKeyboardRemove())
        bot.send_message(chat_id, "<b>Ma'lumotlarnigizni o'zgartiring!</b>", reply_markup=settings_buttons())


# -----------------------------------------------------------------------------------------------------------------
