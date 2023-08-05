import requests
import time


class Telegram:
    def __init__(self, token):
        self.token = token
        self.web = f"https://api.telegram.org/bot{token}/"

    def send_message(self, chat, text):
        msg = {
            "chat_id": chat,
            "text": text
        }
        requests.post(self.web + "sendMessage", json=msg)

    def run(self):
        while True:
            r = requests.post(self.web + "getUpdates")
            time.sleep(0.25)
            print(r)