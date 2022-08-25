import os
import time
import random
import vk_api
from tools import Tools

d = {'`': 'ё', 'q': 'й', 'w': 'ц', 'e': 'у', 'r': 'к', 't': 'е', 'y': 'н', 'u': 'г', 'i': 'ш', 'o': 'щ', 'p': 'з', '[': 'х', ']': 'ъ', 'a': 'ф', 's': 'ы', 'd': 'в', 'f': 'а', 'g': 'п', 'h': 'р', 'j': 'о', 'k': 'л', 'l': 'д', ';': 'ж', "'": 'э', 'z': 'я', 'x': 'ч', 'c': 'с', 'v': 'м', 'b': 'и', 'n': 'т', 'm': 'ь', ',': 'б'}

help_message = "Шило мыло хуй, позвольте представиться, я -- Блябот 😈\n"\
"Что я умею? Исправлять ваши ошибки молодости, желать спокойной ночи, считать моменты и (не)многое другое.\n"\
"Скажу сразу -- женщину найти не смогу, я же не бот дайвинчика, хотя по сути тот же кусок говнокода.\n\n"\
"В общем, ебаный сыр, вот список команд: \n"\
"   🤣 фак, делается ответом на сообщение (переводит ваши проблемы с раскладкой)\n"\
"	😎 закрепролл (проверяет, достоин ли ваш высер висеть в закрепе)\n"\
"	🐊 рулетка (с вероятностью 1/6 кикает тебя из конфы)\n"\
"	🥀 момент, делается ответом на сообщение автора момента (например \"блябот момент (ответ на сообщение)\")\n"\
"	👀 момент рейтинг (выводит топ моментов)\n"\
"   🇦🇲 анек (саратовский армянин расскажет вам рандомную ржаку)\n\n"\
"Команды прописываются в формате \"блябот команда\" если не указано обратное. Например \"блябот фак\"."\

moment_stat = "Топ моментов:\n\n"

class Poebot(object):
    def __init__(self, vk) -> None:
        self.vk = vk
        self.tools = Tools()

    def help(self, peer_id):
        self.vk.method("messages.send", {'peer_id': peer_id, 'message': help_message, 'random_id': random.randint(-2147483648, 2147483647)})   

    def ping(self, peer_id):     
        self.vk.method("messages.send", {'peer_id': peer_id, 'message': 'pong', 'random_id': random.randint(-2147483648, 2147483647)})
    
    def nocommand(self, peer_id):
        self.vk.method("messages.send", {'peer_id': peer_id, 'message': 'каво? пиши блябот помощь и не еби мозг', 'random_id': random.randint(-2147483648, 2147483647)})

    def dm(self, peer_id):
        self.vk.method("messages.send", {'peer_id': peer_id, 'message': "хули палишь шмыга, я только по конфам работаю", 'random_id': random.randint(-2147483648, 2147483647)})

    def fuck(self, obj, peer_id):
        if obj.reply_message:
            converted = ''
            if obj['reply_message']['text'].lower() != '':
                        text = obj['reply_message']['text'].lower()
            else:
                if len(obj['reply_message']['fwd_messages']) != 0:
                        text = ''
                        for i in obj['reply_message']['fwd_messages']:
                            text = text + i['text'] + '\n' 
                        text.lower()
                else:
                    if obj['fwd_messages'][0]['text'] != '':
                        text = ''
                        for i in obj['fwd_messages']:
                            text = text + i['text'] + '\n' 
                        text.lower()

            for i in text:
                try:
                    converted = converted + d[i]
                except:
                    converted = converted + i
            self.vk.method("messages.send", {'peer_id': peer_id, 'message': converted, 'random_id': random.randint(-2147483648, 2147483647)})
        else:
            self.vk.method("messages.send", {'peer_id': peer_id, 'message': 'чувак, fuck делается ответом на сообщение', 'random_id': random.randint(-2147483648, 2147483647)})

    def anec(self, peer_id):
        count = len(os.listdir("anecdotes/"))
        x = random.randint(1, count)
        path = "anecdotes/" + str(x) + ".ogg"

        attach = self.tools.uploadVoice(self.vk, peer_id, path)

        self.vk.method("messages.send", {'peer_id': peer_id, 'attachment': attach, 'random_id': random.randint(-2147483648, 2147483647)})

    def sleep(self, peer_id, user_id):
        user_get = self.vk.method('users.get', {'user_ids': user_id, 'random_id': random.randint(-2147483648, 2147483647)})
        user = user_get[0]['first_name'] + ' ' + user_get[0]['last_name']
        message = 'Спокойной ночи, @id' + str(user_id) + " (" + user + ")"
        count = len(os.listdir("cats/"))

        cat = random.randint(1, count)
        path = "cats/" + str(cat) + ".jpeg"

        attach = self.tools.uploadPhoto(self.vk, path)

        self.vk.method("messages.send", {'peer_id': peer_id, 'message': message, 'attachment': attach, 'random_id': random.randint(-2147483648, 2147483647)})

    def pinroll(self, obj, peer_id, msg_id, cmsg_id):
        if obj.reply_message:
            if random.choice([True, False]):
                self.vk.method("messages.pin", {"peer_id": peer_id, "message_id": obj.reply_message["id"], "conversation_message_id": obj.reply_message["conversation_message_id"], "random_id": random.randint(-2147483648, 2147483647)})
            else:
                self.vk.method("messages.send", {'peer_id': peer_id, 'message': "сегодня просто не твой день", 'random_id': random.randint(-2147483648, 2147483647)})
    def roulette(self, peer_id, user_id):
        drum = [0, 0, 0, 0, 0, 0]
        random.seed(time.time())
        x = random.randint(0, 5)
        drum[x] = 1

        shot = random.choice(drum)
        if shot:
            self.vk.method("messages.removeChatUser", {"chat_id": peer_id-2000000000, "user_id": user_id, "random_id": random.randint(-2147483648, 2147483647)})
            self.vk.method("messages.send", {'peer_id': peer_id, 'message': "упс", 'random_id': random.randint(-2147483648, 2147483647)})
        else:
            self.vk.method("messages.send", {'peer_id': peer_id, 'message': "повезло повезло", 'random_id': random.randint(-2147483648, 2147483647)})

    def newmoment(self, obj):
        if obj.reply_message:
            user_get = self.vk.method('users.get', {'user_ids': obj['reply_message']['from_id'], 'random_id': random.randint(-2147483648, 2147483647)})
            user = user_get[0]['first_name'] + ' ' + user_get[0]['last_name']
            chat_id = obj.peer_id
            result = self.tools.insertSQL(chat_id - 2000000000, obj['reply_message']['from_id'], user)
            self.vk.method("messages.send", {'peer_id': chat_id, 'message': result, 'random_id': random.randint(-2147483648, 2147483647)})

    def momentstat(self, peer_id): 
        moment_stat = "Топ моментов:\n\n" + self.tools.selectSQL(peer_id - 2000000000)
        self.vk.method("messages.send", {'peer_id': peer_id, 'message': moment_stat, 'random_id': random.randint(-2147483648, 2147483647)})


# ------------------------ UNUSED COMMANDS ------------------------ 

    def artyom():
        now = datetime.now()
        date = datetime.strptime('9 February 2020', '%d %B %Y')
        return('Артем должен Гоше уже ' + str((now - date).days) + ' дней')

    def me(obj):
        text = obj.text
        user_id = obj.from_id
        user_inf = vk.method('users.get', {'user_ids': user_id, 'random_id': random.randint(-2147483648, 2147483647)})
        user = user_inf[0]['first_name'] + ' ' + user_inf[0]['last_name']
        return(user + ' ' + text[4:])

    def todo(obj):
        user_get = vk.method('users.get', {'user_ids': obj.from_id, 'random_id': random.randint(-2147483648, 2147483647)})
        user = user_get[0]['first_name'] + ' ' + user_get[0]['last_name']
        text = obj.text[6:]
        splitted_txt = re.split(r'[*]', text)
        p1 = splitted_txt[0].strip()
        p2 = splitted_txt[1].strip()
        return('"' + p1 + '" — сказал ' + user + ' и ' + p2)

# ------------------------ UNUSED COMMANDS ------------------------ 