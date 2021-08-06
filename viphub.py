from telegram.ext import Updater
import logging
from telegram.ext import CommandHandler



ADMIN_ID = 800882871 #user_id of sender of file and broadcaster

def membercounter():
    pass



def start(update, context):
    message_text = update.message.text
    if(len(message_text) > 6):
        print(message_text[7:])

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
