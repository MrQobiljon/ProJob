from data.loader import bot, db

import handlers

db.create_user_table()
db.create_table_works()
db.create_table_directions()
db.create_table_admins()

if __name__ == '__main__':
    print("Bot ishga tushdi 👉", 'https://t.me/projobuz_bot')
    bot.polling(none_stop=True)