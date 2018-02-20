import telebot
from random import randint
import pymysql
from time import sleep
bot = telebot.TeleBot('APIKEY')

pool = []


def get_random_message(list):
    sleep(randint(2, 5))
    return list[randint(0, len(list) - 1)]


def remove_symbols(msg):
    sym = '%\\;\''
    res = msg
    for i in msg:
        if i in sym:
            res = res.replace(i, '')
    return res


def zhri_ego_eblo_tupoe(msg, chatid):
    insert = 'INSERT INTO data SET message=\'' + remove_symbols(msg) + '\', keywords=\''
    select = 'SELECT message FROM data WHERE '
    for i in msg.split(' '):
        if len(remove_symbols(i)) > 3:
            i_keys = remove_symbols(i).split(' ')
            if insert != 'INSERT INTO data SET message=\'' + remove_symbols(msg) + '\', keywords=\'':
                insert += ','
            if select != 'SELECT message FROM data WHERE ':
                select += ' OR '
            for k in i_keys:
                insert += k.lower()
                select += 'keywords LIKE \'%' + k.lower() + '%\''
    insert += '\''

    print(insert)
    print(select)
    print('----------------------------------------------')

    conn = pymysql.connect(host='127.0.0.1', port=
    3306, user='root',
                           passwd='root', db='tgbot', use_unicode=True, charset="utf8")

    cur = conn.cursor()
    try:
        cur.execute(select)
        if cur.rowcount:
            answers = []
            for row in cur:
                answers.append(row[0])
            print(answers)
            try:
                bot.send_message(chatid, get_random_message(answers))
            except:
                pass
       
        try:
            cur.execute(insert)
            conn.commit()
        except Exception as e:
            print('***********************************')
            print(e)
            print('***********************************')

    except Exception as e:

        print('***********************************')

        print(e)

        print('***********************************')
    finally:
        conn.close()
        cur.close()





@bot.message_handler(content_types=["text"])
def handle_message(message):
    '''

        bot.send_message(message.chat.id, get_random_message(pool))
    '''
    print('******')
    print('CHAT_ID: ' + str(message.chat.id))
    print('******')
    if '@' in message.text or len(message.text) > 300 or 'чилен' in message.text.lower():
        pass
    else:
        rnd = randint(0, 999)
        if rnd % 2 == 0:
            try:
                zhri_ego_eblo_tupoe(message.text, message.chat.id)
            except Exception as e:
                print(e)

while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print('***********************************')
        print(e)
        print('***********************************')
        sleep(15)

