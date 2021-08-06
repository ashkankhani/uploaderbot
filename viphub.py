from telegram.ext import Updater
import logging
from telegram.ext import CommandHandler,Filters
import sqlite3
from random import sample






ADMIN_ID = 800882871 #user_id of sender of file and broadcaster
characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'



def broadcast(update , context):
    print('broad')
    



def stats(update,context):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute(f'''select count(id)
    from users
    ''')
    users_count = (cursor.fetchone())[0]
    context.bot.send_message(chat_id = update.message.chat.id , text = f'''آمار کاربران ربات:
{users_count} نفر میباشد
    
    
''')
    


def add_file_to_db(code , message_id):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute(f'''select count(id)
    from links
    ''')
    files_count = (cursor.fetchone())[0]

    cursor.execute(f'''insert into links
    values
    ({files_count + 1} , '{code}' , {message_id})
    ''')
    connection.commit()


def random_name():
    name = ''.join(sample(characters , 10))
    return name


def user_in_db(user_id):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute(f'''select id 
    from users
    where user_id = {user_id}
    ''')
    if(cursor.fetchone()):
        return True
    else:
        return False


def add_user_to_db(user_id , fname , lname):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute(f'''select count(id)
    from users
    ''')
    users_count = (cursor.fetchone())[0]
    cursor.execute(f'''insert into users
    values
    ({users_count + 1} , {user_id} , '{fname}' , '{lname}')
    ''')
    connection.commit()




def get_file_id(file_code):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute(f'''select message_id 
    from links
    where code = '{file_code}'
    ''')
    res = cursor.fetchone()
    if(res):
        return res[0]
    else:
        return None

def send_file(file_id,context):
    context.bot.copy_message(chat_id = ADMIN_ID , from_chat_id = ADMIN_ID , message_id = file_id)
    




def start(update, context):
    message_text = update.message.text
    user_id = update.message.chat.id
    if not (user_in_db(user_id)):
        add_user_to_db(user_id , update.message.chat.first_name , update.message.chat.last_name)
    
    if(len(message_text) > 6):
        #donbale file taraf
        flie_code = message_text[7:]
        file_id = get_file_id(flie_code)
        if(file_id):
            send_file(file_id , context)
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text="فایل مورد نظر وجود ندارد!")


    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="سلام به ربات ما خوش اومدی!")


def add_file(update , context):
    if(update.message.reply_to_message):
        file_code = random_name()
        message_id = update.message.reply_to_message.message_id
        add_file_to_db(file_code , message_id)
        context.bot.send_message(chat_id=ADMIN_ID, text=f'''فایل با موفقیت به ربات افزوده شد!
لینک فایل:
https://t.me/telexviphubbot?start={file_code}        
        
        ''')
    else:
        context.bot.send_message(chat_id=ADMIN_ID, text="روی فایل مورد نظر ریپلای کنین!")


def main():

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    updater = Updater(token='1917460438:AAHRJ3v45s4Pcs_wvlv-Hw64w8_Maj9kTOc', use_context=True,workers=200)


    dispatcher = updater.dispatcher



    start_handler = CommandHandler('start', start,run_async=True)
    add_file_handler = CommandHandler('add' , add_file , filters=Filters.chat(ADMIN_ID))
    stats_handler = CommandHandler('stats' , stats , filters=Filters.chat(ADMIN_ID))
    broadcast_handler = CommandHandler('broadcast' , broadcast , filters=Filters.chat(ADMIN_ID))
    dispatcher.add_handler(add_file_handler)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(stats_handler)
    dispatcher.add_handler(broadcast_handler)



    updater.start_polling()

if(__name__ == '__main__'):
    main()
