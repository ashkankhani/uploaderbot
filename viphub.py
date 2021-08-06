from telegram.ext import Updater
import logging
from telegram.ext import CommandHandler
import sqlite3






ADMIN_ID = 800882871 #user_id of sender of file and broadcaster

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
    res = (cursor.fetchone())[0]
    return res

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
        send_file(file_id , context)

    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="سلام به ربات ما خوش اومدی!")





def main():

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    updater = Updater(token='1917460438:AAHRJ3v45s4Pcs_wvlv-Hw64w8_Maj9kTOc', use_context=True)


    dispatcher = updater.dispatcher



    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)


    updater.start_polling()

if(__name__ == '__main__'):
    main()
