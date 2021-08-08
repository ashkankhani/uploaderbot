from telegram.ext import Updater,CommandHandler,Filters,CallbackQueryHandler,UpdateFilter,MessageHandler
import logging
from telegram import InlineKeyboardButton,InlineKeyboardMarkup
import sqlite3
from random import sample
from time import sleep
from telegram import User

from telegram.constants import PARSEMODE_MARKDOWN_V2








ADMIN_ID = 365527971 #sudo user id
characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'


def backup_data(update,context):
    admin_id = update.message.chat.id
    context.bot.send_document(chat_id = admin_id , document = open('database.db', 'rb') , filename = 'database.db')


def admin_help(update,context):
    update.message.reply_text('''دستورات ربات:
/help : جهت راهنمایی و نمایش دستورات
/setadmin [with reply] : جهت ادمین کردن لیستی از آیدی های عددی
/join [with reply] : جهت اضافه کردن لیستی از آیدی های عددی کانال ها به جوین اجباری
/add [with reply] : جهت اضافه کردن فایل مورد نظر و ذخیره سازی آن
/stats : جهت آمارگیری
/boradcast [with reply] : جهت ارسال پیام همگانی
/deleteon جهت روشن کردن حذف خودکار فایل پس از کذشت یک دقیقه بعد از ارسال
/deleteoff جهت خاموش کردن حذف خودکار فایل پس از کذشت یک دقیقه بعد از ارسال
/backup جهت دریافت فایل دیتابیس ربات
/joinon جهت روشن کردن جوین اجباری
/joinoff جهت خاموش کردن جوین اجباری
''')


def is_force_join_on():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute(f'''select force_join 
    from settings
    ''')
    res = (cursor.fetchone())[0]
    return res


def force_join_on(update,context):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute(f'''update settings
    set force_join = 1
    ''')
    connection.commit()
    update.message.reply_text('جوین اجباری با موفقیت فعال شد')

def force_join_off(update,context):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute(f'''update settings
    set force_join = 0
    ''')
    connection.commit()
    update.message.reply_text('جوین اجباری با موفقیت غیر فعال شد')

def auto_delete_on(update,context):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute(f'''update settings
    set auto_delete = 1
    ''')
    connection.commit()
    update.message.reply_text('حذف خودکار با موفقیت فعال شد')

def auto_delete_off(update,context):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute(f'''update settings
    set auto_delete = 0
    ''')
    connection.commit()
    update.message.reply_text('حذف خودکار با موفقیت غیر فعال شد')

def is_auto_delete_on():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute(f'''select auto_delete 
    from settings
    ''')
    res = (cursor.fetchone())[0]
    return res





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
    update.message.reply_text('لیست جوین اجباری با موفقیت به روز شد!\nتوجه کنید که ربات حتما باید در کانال مربوطه ادمین شود و در غیر اینصورت با خطا مواجه میشوید')

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




def forward(context,message_id,admin_id):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute(f'''select user_id
    from users
    ''')
    user_list = cursor.fetchall()
    for tup in user_list:
        context.bot.forward_message(chat_id = tup[0] , from_chat_id = admin_id , message_id = message_id)



def copy(context,message_id,admin_id):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute(f'''select user_id
    from users
    ''')
    user_list = cursor.fetchall()
    for tup in user_list:
        context.bot.copy_message(chat_id = tup[0] , from_chat_id = admin_id , message_id = message_id)


def button(update , context):
    query = update.callback_query
    way = (query.data).split(',')
    message_id = way[2]
    admin_id = way[3]
    
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
        forward(context,message_id,admin_id)
    if(way[1] == '2'):
        copy(context,message_id,admin_id)
    context.bot.send_message(chat_id = admin_id , text = 'ارسال با موفقیت انجام شد!')


    

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

def send_file(file_id,user_id,file_code,context):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute(f'''select from_admin 
    from links
    where code = '{file_code}'
    ''')
    from_admin = (cursor.fetchone())[0]
    sended_file = context.bot.copy_message(chat_id = user_id , from_chat_id = from_admin , message_id = file_id)
    if(is_auto_delete_on()):
        context.bot.send_message(chat_id = user_id , text = 'این فایل بعد از 60 ثانیه حذف میشود.پس قبل از حذف آن را ذخیره کنید')
        sleep(60)
        context.bot.delete_message(chat_id = user_id , message_id = sended_file.message_id)
    
    
    
    


def joined_button(update,context):
    query = update.callback_query
    way = ((query.data).split(','))[1:]
    file_id , file_code , user_id = way
    if(not is_joined(context,user_id)):
        context.bot.send_message(chat_id = user_id , text = 'شما عضو چنل نیستید')
        return 0

    if(file_id != 'None'):
        send_file(file_id ,user_id, file_code ,context)
    else:
        context.bot.send_message(chat_id = user_id , text = 'فایل مورد نظر یافت نشد!')


    
    

def join_to_our_channle(list_of_invite_links,update,file_id,user_id,file_code):
    shomaresh = ['اول','دوم','سوم','چهارم','پنجم']
    keyboard = [

    ]
    for i in range(0,len(list_of_invite_links)):
        channle_button_base = [InlineKeyboardButton(f'عضویت در کانال {shomaresh[i]}',url = list_of_invite_links[i])]
        keyboard.append(channle_button_base)

    keyboard.append([InlineKeyboardButton('عضو شدم',callback_data =f'j,{file_id},{file_code},{user_id}')])

    
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(text = 'ابتدا وارد کانال های زیر شده و سپس روی دکمه عضو شدم کلیک کنید:',reply_markup = reply_markup)

def convert_id_to_invite(context):
    channle_links = []
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute(f'''select channle_id 
    from join_channles
    ''')
    channle_ids = cursor.fetchall()

    for channle_id in channle_ids:
        channle_links.append((context.bot.getChat(channle_id[0])).invite_link)  


    return channle_links
        

    



def start(update, context):
    message_text = update.message.text
    user_id = update.message.chat.id
    if not (user_in_db(user_id)):
        add_user_to_db(user_id , update.message.chat.first_name , update.message.chat.last_name)
    file_code = message_text[7:]
    file_id = get_file_id(file_code)
    if(not(is_force_join_on() and (not is_joined(context , user_id)))):
        if(file_id):
            send_file(file_id ,user_id, file_code ,context)
        else:
            update.message.reply_text(text="فایل مورد نظر وجود ندارد!")

    else:
        list_of_invite_links = convert_id_to_invite(context)
        join_to_our_channle(list_of_invite_links,update,file_id,user_id,file_code)
        



def add_file(update , context):
    
    file_code = random_name()
    message_id = update.message.reply_to_message.message_id
    add_file_to_db(file_code , message_id , update.message.chat.id)
    update.message.reply_text(text=f'''فایل با موفقیت به ربات افزوده شد!
لینک فایل:
https://t.me/Yahodupload_bot?start={file_code}        
    
    ''')

def welcome(update , context):
    user_id = update.message.chat.id
    user_mention = User(user_id ,first_name = update.message.chat.first_name,is_bot = False).mention_markdown_v2()
    update.message.reply_text(f'''سلام {user_mention}
دوست عزیزم به ربات یهود 🐕  آپلودر خوش آمدید 🌺''',parse_mode =PARSEMODE_MARKDOWN_V2)
    if not (user_in_db(user_id)):
        add_user_to_db(user_id , update.message.chat.first_name , update.message.chat.last_name)
    

    


def main():

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    updater = Updater(token='1936804982:AAEjadVwiSQ6IdhEWSw7T34gJHDj4PRwbeU', use_context=True,workers=200)


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
    help_handler = CommandHandler('help' , admin_help , filters=isadminator,run_async=True)
    backup_data_handler = CommandHandler('backup' , backup_data , filters=isadminator,run_async=True)
    admin_handler = CommandHandler('setadmin' , admin_settings , filters=Filters.chat(ADMIN_ID),run_async=True)
    join_handler = CommandHandler('join',join_settings, filters=isadminator & Filters.reply,run_async=True)
    welcomehandler = CommandHandler('start' , welcome , filters=~isredirected,run_async=True)
    start_handler = CommandHandler('start', start,filters = isredirected,run_async=True)
    add_file_handler = CommandHandler('add' , add_file , filters=isadminator & Filters.reply,run_async=True)
    stats_handler = CommandHandler('stats' , stats , filters=isadminator,run_async=True)
    broadcast_handler = CommandHandler('broadcast' , broadcast , filters=isadminator & Filters.reply,run_async=True)
    auto_delete_on_handler = CommandHandler('deleteon' , auto_delete_on , filters=isadminator,run_async=True)
    auto_delete_off_handler = CommandHandler('deleteoff' , auto_delete_off , filters=isadminator,run_async=True)
    button_handler = CallbackQueryHandler(button,pattern= '^b.*$',run_async=True)
    button_joined_handler = CallbackQueryHandler(joined_button,pattern= '^j.*$',run_async=True)
    force_join_on_handler = CommandHandler('joinon' , force_join_on , filters=isadminator,run_async=True)
    force_join_off_handler = CommandHandler('joinoff' , force_join_off , filters=isadminator,run_async=True)
    dispatcher.add_handler(add_file_handler)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(stats_handler)
    dispatcher.add_handler(broadcast_handler)
    dispatcher.add_handler(button_handler)
    dispatcher.add_handler(welcomehandler)
    dispatcher.add_handler(join_handler)
    dispatcher.add_handler(admin_handler)
    dispatcher.add_handler(button_joined_handler)
    dispatcher.add_handler(auto_delete_on_handler)
    dispatcher.add_handler(auto_delete_off_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(backup_data_handler)
    dispatcher.add_handler(force_join_on_handler)
    dispatcher.add_handler(force_join_off_handler)

    




    updater.start_polling()

if(__name__ == '__main__'):
    main()
