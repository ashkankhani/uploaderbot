from random import sample






ADMIN_ID = 800882871 #user_id of sender of file and broadcaster
characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

def random_name():
    print(sample(characters , 10))


random_name()