# -*- coding: utf-8 -*-

import re
import time
import vk_api
import random
import requests
import traceback
from cgitb import text
from get import VKConfig
from commands import Poebot
from datetime import datetime
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType


# Object creation
conf = VKConfig() 

vk = conf.getVK()
longpoll = conf.getLongpoll()

poebot = Poebot(vk)

def switch(command, obj):
    user_id = obj.from_id
    msg_id = obj.id
    cmsg_id = obj.conversation_message_id

    if command == "пинг":
        poebot.ping(peer_id)
    elif command == "помощь":
        poebot.help(peer_id)
    elif command == "фак":
        poebot.fuck(obj, peer_id)
    elif command == "закрепролл":
        poebot.pinroll(obj, peer_id, msg_id, cmsg_id)
    elif command == "рулетка":
        poebot.roulette(peer_id, user_id)
    elif command == "анек":
        poebot.anec(peer_id)
    elif command == "момент":
        poebot.newmoment(obj)
    elif command == "рейтинг":
        poebot.momentstat(peer_id)
    else:
        poebot.nocommand(peer_id)

while True:
    try:
        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                msg_id = event.object.conversation_message_id
                peer_id = event.object.peer_id
                obj = event.object 
                msg_text = event.object.text.lower()
                
                # Контентыч из бесед
                if event.object.peer_id != event.object.from_id:  
                    textArray = event.object.text.lower().split()  
                    if textArray[0] == "блябот" and len(textArray) > 1:
                        switch(textArray[1], obj)
                    
                    if msg_text == "я спать":
                        poebot.sleep(peer_id, event.object.from_id)

                # Контентыч из лички
                elif event.object.peer_id == event.object.from_id:
                    poebot.dm(event.object.from_id)

    except Exception as e:
        traceback.print_exc()
        time.sleep(1)

# Поток 1 -- обработка сообщений и команд
# Поток 2 -- логирование
# Поток 3 -- барбот кок
