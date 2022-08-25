import vk_api
import sqlite3
import requests

insert_sql = """INSERT INTO moment VALUES ({chat_id}, {vk_id}, '{name}', {num});"""
select_sql = """SELECT * FROM moment WHERE chat_id = {chat_id} ORDER BY quantity DESC;"""
select_user_sql = """SELECT * FROM moment WHERE chat_id = {chat_id} AND vk_id = {vk_id};"""
update_sql = """UPDATE moment SET quantity = quantity + 1 WHERE chat_id = {chat_id} AND vk_id = {vk_id}"""
get_moment_sql = """SELECT quantity FROM moment WHERE chat_id = {chat_id} AND vk_id = {vk_id}"""

class Tools(object):
    db_name = "poebot.db"

    def uploadPhoto(self, vk, file):
        upload = vk.method("photos.getMessagesUploadServer")
        r = requests.post(upload['upload_url'], files={'photo': open(file, 'rb')}).json()
        save = vk.method('photos.saveMessagesPhoto', {'photo': r['photo'], 'server': r['server'], 'hash': r['hash']})
        owner_id = save[0]["owner_id"]
        id_own = save[0]["id"]
        attachment ='photo{}_{}'.format(owner_id,id_own)
        return(attachment)
    
    def uploadVoice(self, vk, user_id, file):
        upload = vk.method("docs.getMessagesUploadServer", {'type': 'audio_message', 'peer_id': user_id})
        r = requests.post(upload['upload_url'], files={'file': open(file, 'rb')}).json()
        save = vk.method('docs.save', {'file': r['file']})
        v = 'audio_message{}_{}'.format(save['audio_message']['owner_id'], save['audio_message']['id'])
        return v

    def selectSQL(self, id):
        rows = ""
        try:
            sqlite_connection = sqlite3.connect('poebot.db')
            cursor = sqlite_connection.cursor()

            cursor.execute(select_sql.format(chat_id = id))
            records = cursor.fetchall()
            
            for row in records:
                rows += row[2] + " - " + str(row[3]) + " 🥀\n"
            

            cursor.close()

        except sqlite3.Error as error:
            print(error)

        finally:
            if (sqlite_connection):
                sqlite_connection.close()
                print("Соединение с SQLite закрыто")

        return rows

    def insertSQL(self, chat_id, vk_id, name):
        try:
            sqlite_connection = sqlite3.connect('poebot.db')
            cursor = sqlite_connection.cursor()

            
            cursor.execute(select_user_sql.format(chat_id = chat_id, vk_id = vk_id))
            records = cursor.fetchall()
            
            if len(records) == 0:
                cursor.execute(insert_sql.format(chat_id = chat_id, vk_id = vk_id, name = name, num = 1))
                sqlite_connection.commit()
                cursor.close()

                return "🥀 Поздравляю с первым моментом, " + name
            
            else:
                cursor.execute(update_sql.format(chat_id = chat_id, vk_id = vk_id))
                sqlite_connection.commit()

                cursor.execute(get_moment_sql.format(chat_id = chat_id, vk_id = vk_id))
                user_moment = cursor.fetchall()


                cursor.close()
                return "🥀 Количество моментов пользователя " + name + ": " + str(user_moment[0][0])

        except sqlite3.Error as error:
            print(error)

        finally:
            if (sqlite_connection):
                sqlite_connection.close()
                print("Соединение с SQLite закрыто")