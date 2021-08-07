from telegram.ext import Updater,CommandHandler,Filters,CallbackQueryHandler,UpdateFilter,MessageHandler
import logging
from telegram import InlineKeyboardButton,InlineKeyboardMarkup
import sqlite3
from random import sample







ADMIN_ID = 800882871 #user_id of sender of file and broadcaster
characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'





#def is_joined(user_id):
  #  connection = sqlite3.connect('database.db')
   # cursor = connection.cursor()
  #  cursor.execute(f'''select channle_id
  #  from join_channles
   # ''')
   # channle_list = cursor.fetchall()
   # for tup in channle_list:
    #    pass
 #

def test(update,context):
    print('join nisti')


def forward(context,message_id):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute(f'''select user_id
    from users
    ''')
    user_list = cursor.fetchall()
    for tup in user_list:
        context.bot.forward_message(chat_id = tup[0] , from_chat_id = ADMIN_ID , message_id = message_id)



def copy(context,message_id):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute(f'''select user_id
    from users
    ''')
    user_list = cursor.fetchall()
    for tup in user_list:
        context.bot.copy_message(chat_id = tup[0] , from_chat_id = ADMIN_ID , message_id = message_id)


def button(update , context):
    query = update.callback_query
    way = query.data
    message_id = way[2:]
    
    if(way[1] == '1'):
        gozine = 'ارسال همگانی با فوروارد'
    elif(way[1] == '2'):
        gozine = 'ارسال همگانی عادی'
    else:
        query.edit_message_text(text = 'عملیات لغو شد')
        return 0

    query.edit_message_text(text = f'''گزینه انتخابی:{gozine}
در حال ارسال پیام به کاربران...''')
    if(way[1] == '1'):
        forward(context,message_id)
    if(way[1] == '2'):
        copy(context,message_id)
    context.bot.send_message(chat_id = ADMIN_ID , text = 'ارسال با موفقیت انجام شد!')


    

def broadcast(update , context):
    keyboard = [
        [InlineKeyboardButton('ارسال همگانی با فوروارد',callback_data =f'b1{update.message.reply_to_message.message_id}')],
        [InlineKeyboardButton('ارسال همگانی عادی',callback_data = f'b2{update.message.reply_to_message.message_id}')],
        [InlineKeyboardButton('لغو عملیات',callback_data = f'b3{update.message.reply_to_message.message_id}')],

    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(text = 'لطفا نوع ارسال را مشخص نمایید:',reply_markup = reply_markup)
    
    



def stats(update,context):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute(f'''select count(id)
    from users
    ''')
    users_count = (cursor.fetchone())[0]
    update.message.reply_text(text = f'''آمار کاربران ربات:
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
            update.message.reply_text(text="فایل مورد نظر وجود ندارد!")


    else:
        update.message.reply_text(text="سلام به ربات ما خوش اومدی!")


def add_file(update , context):
    
    file_code = random_name()
    message_id = update.message.reply_to_message.message_id
    add_file_to_db(file_code , message_id)
    update.message.reply_text(text=f'''فایل با موفقیت به ربات افزوده شد!
لینک فایل:
https://t.me/telexviphubbot?start={file_code}        
    
    ''')
    


def main():

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    updater = Updater(token='1917460438:AAHRJ3v45s4Pcs_wvlv-Hw64w8_Maj9kTOc', use_context=True,workers=200)


    dispatcher = updater.dispatcher

    class Getting_member(UpdateFilter):
        def filter(self, update):

            chat_id = update.effective_chat.id
            print(chat_id)
            getChatMember = updater.bot.getChatMember(-1001494317651, chat_id)

            if getChatMember.status == 'left':
                return True
            return False

    GettingMember = Getting_member()
    updater.dispatcher.add_handler(MessageHandler((Filters.all  & (~GettingMember  )), test))



    start_handler = CommandHandler('start', start,run_async=True)
    add_file_handler = CommandHandler('add' , add_file , filters=Filters.chat(ADMIN_ID) & Filters.reply)
    stats_handler = CommandHandler('stats' , stats , filters=Filters.chat(ADMIN_ID))
    broadcast_handler = CommandHandler('broadcast' , broadcast , filters=Filters.chat(ADMIN_ID) & Filters.reply)
    button_handler = CallbackQueryHandler(button,pattern= '^b.*$')
    dispatcher.add_handler(add_file_handler)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(stats_handler)
    dispatcher.add_handler(broadcast_handler)
    dispatcher.add_handler(button_handler)



    updater.start_polling()

if(__name__ == '__main__'):
    main()
