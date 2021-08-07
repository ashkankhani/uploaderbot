from telegram.ext import Updater,CommandHandler,Filters,CallbackQueryHandler,UpdateFilter,MessageHandler
import logging
from telegram import InlineKeyboardButton,InlineKeyboardMarkup
import sqlite3
from random import sample







ADMIN_ID = 800882871 #sudo user id
characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'


def admin_settings(update,context):
    admin_text_list = update.message.reply_to_message.text
    list_of_admin = list_maker(admin_text_list)
    add_admin_to_db(list_of_admin)
    update.message.reply_text('لیست ادمین با موفقیت به روز شد!')

def add_admin_to_db(list_of_admin):
    admin_count = len(list_of_admin)
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute(f'''delete 
    from admins
    ''')
    for i in range(1 , admin_count + 1):
        cursor.execute(f'''insert into admins
        values
        ({i} , {list_of_admin[i - 1]})
    ''')
    connection.commit()



def join_settings(update,context):
    channle_text_list = update.message.reply_to_message.text
    list_of_channle = list_maker(channle_text_list)
    add_channle_to_db(list_of_channle)
    update.message.reply_text('لیست جوین اجباری با موفقیت به روز شد!')

def list_maker(channle_text_list):
    list_of_ids = channle_text_list.split('\n')
    for i in range(0,len(list_of_ids)):
        list_of_ids[i] = int(list_of_ids[i])

    return list_of_ids


def add_channle_to_db(list_of_channle):
    channle_count = len(list_of_channle)
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute(f'''delete 
    from join_channles
    ''')
    for i in range(1 , channle_count + 1):
        cursor.execute(f'''insert into join_channles
        values
        ({i} , {list_of_channle[i - 1]})
    ''')
    connection.commit()





def is_joined(context,user_id):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute(f'''select channle_id
    from join_channles
    ''')
    channle_list = cursor.fetchall()
    joined = True
    for tup in channle_list:
        getChatMember = context.bot.getChatMember(chat_id = tup[0], user_id = user_id)
        if getChatMember.status == 'left':
            joined = False
            break
    return joined




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
        [InlineKeyboardButton('ارسال همگانی با فوروارد',callback_data =f'b,1,{update.message.reply_to_message.message_id},{update.message.chat.id}')],
        [InlineKeyboardButton('ارسال همگانی عادی',callback_data = f'b,2,{update.message.reply_to_message.message_id},{update.message.chat.id}')],
        [InlineKeyboardButton('لغو عملیات',callback_data = f'b,3,{update.message.reply_to_message.message_id},{update.message.chat.id}')],

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
    


def add_file_to_db(code , message_id ,from_admin):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute(f'''select count(id)
    from links
    ''')
    files_count = (cursor.fetchone())[0]

    cursor.execute(f'''insert into links
    values
    ({files_count + 1} , '{code}' , {message_id} , {from_admin})
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

def send_file(file_id,user_id,context):
    context.bot.copy_message(chat_id = user_id , from_chat_id = ADMIN_ID , message_id = file_id)
    




def start(update, context):
    message_text = update.message.text
    user_id = update.message.chat.id
    if not (user_in_db(user_id)):
        add_user_to_db(user_id , update.message.chat.first_name , update.message.chat.last_name)
    
    if(is_joined(context , user_id)):
        flie_code = message_text[7:]
        file_id = get_file_id(flie_code)
        if(file_id):
            send_file(file_id ,user_id, context)
        else:
            update.message.reply_text(text="فایل مورد نظر وجود ندارد!")



def add_file(update , context):
    
    file_code = random_name()
    message_id = update.message.reply_to_message.message_id
    add_file_to_db(file_code , message_id , update.message.chat.id)
    update.message.reply_text(text=f'''فایل با موفقیت به ربات افزوده شد!
لینک فایل:
https://t.me/telexviphubbot?start={file_code}        
    
    ''')

def welcome(update , context):
    user_id = update.message.chat.id
    update.message.reply_text("سلام به ربات ما خوش اومدی!")
    if not (user_in_db(user_id)):
        add_user_to_db(user_id , update.message.chat.first_name , update.message.chat.last_name)
    

    


def main():

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    updater = Updater(token='1917460438:AAHRJ3v45s4Pcs_wvlv-Hw64w8_Maj9kTOc', use_context=True,workers=200)


    dispatcher = updater.dispatcher


    class is_redirected(UpdateFilter):
        def filter(self , update):
            if(len(update.message.text) > 6):
                return True
            return False

    class is_adminator(UpdateFilter):
        def filter(self , update):
            user_id = update.message.chat.id
            if(user_id == ADMIN_ID):
                return True
            is_admin = False
            connection = sqlite3.connect('database.db')
            cursor = connection.cursor()
            cursor.execute(f'''select admin_id
            from admins
            ''')
            admin_list = cursor.fetchall()

            for tup in admin_list:
                if(user_id == tup[0]):
                    is_admin = True
                    break
            
            return is_admin


    

    
    isredirected = is_redirected()
    isadminator = is_adminator()
    
    admin_handler = CommandHandler('setadmin' , admin_settings , filters=Filters.chat(ADMIN_ID))
    join_handler = CommandHandler('join',join_settings, filters=isadminator & Filters.reply)
    welcomehandler = CommandHandler('start' , welcome , filters=~isredirected)
    start_handler = CommandHandler('start', start,filters = isredirected,run_async=True)
    add_file_handler = CommandHandler('add' , add_file , filters=isadminator & Filters.reply)
    stats_handler = CommandHandler('stats' , stats , filters=isadminator)
    broadcast_handler = CommandHandler('broadcast' , broadcast , filters=isadminator & Filters.reply)
    button_handler = CallbackQueryHandler(button,pattern= '^b.*$')
    dispatcher.add_handler(add_file_handler)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(stats_handler)
    dispatcher.add_handler(broadcast_handler)
    dispatcher.add_handler(button_handler)
    dispatcher.add_handler(welcomehandler)
    dispatcher.add_handler(join_handler)
    dispatcher.add_handler(admin_handler)



    updater.start_polling()

if(__name__ == '__main__'):
    main()
