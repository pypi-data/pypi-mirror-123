import requests


class Telegram:
    def __init__(self, token):
        self.web = f"https://api.telegram.org/bot{token}/"
        if requests.post(self.web + "getUpdates").status_code != 200:
            raise Exception("The api request was not successful")

    def send_message(self, chat, text):
        msg = {
            "chat_id": chat,
            "text": text
        }
        requests.post(self.web + "sendMessage", json=msg)

    def run(self, handle_function=None, debug=False):
        print("* Starting bot and waiting for updates: TELEGRAM")
        if debug:
            print("* Debug mod: ENABLED")
        else:
            print("* Debug mod: DISABLED")
        print()

        offset = 0
        while True:
            r = requests.post(self.web + f"getUpdates?offset={offset}").json()["result"]
            for x in r:
                if debug:
                    print(x["message"])
                if handle_function is not None:
                    handle_function(x["message"])
            if len(r) != 0:
                offset = r[-1]["update_id"] + 1
