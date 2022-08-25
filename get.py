import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType


class VKConfig(object):
    def __init__(self):
        self.vk = vk_api.VkApi(token="")

    def getVK(self):
        return self.vk
        
    def getLongpoll(self):
        self.vk._auth_token()
        self.vk.get_api()

        self.longpoll = VkBotLongPoll(self.vk, )

        return self.longpoll