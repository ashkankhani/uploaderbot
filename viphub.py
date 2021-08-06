from telegram.ext import Updater
import logging
from telegram.ext import CommandHandler
import sqlite3






ADMIN_ID = 800882871 #user_id of sender of file and broadcaster



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
