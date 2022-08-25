import schedule
from time import sleep
from threading import Thread

class Cock(object):
    @staticmethod
    def cock(vk, peer_id):
        vk.method('messages.send', {'peer_id': peer_id, 'message': 'барбот кок', 'random_id': 0})

    def sch():
        schedule.every().day.at('00:00').do(cock, vk, 2000000007)
        while True:
            schedule.run_pending()
            sleep(1)

    def start(self):    
        t = Thread(target=sch)
        t.start()