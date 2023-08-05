import requests


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

    def run(self, debug=False, handle_function=None):
        print("* Starting bot waiting updates")
        if debug:
            print("* Debugging mod enabled")
        print()

        offset = 0
        while True:
            r = requests.post(self.web + f"getUpdates?offset={offset}").json()["result"]
            for x in r:
                if debug:
                    print(x["message"])
                handle_function(x["message"])
            if len(r) != 0:
                offset = r[-1]["update_id"] + 1
