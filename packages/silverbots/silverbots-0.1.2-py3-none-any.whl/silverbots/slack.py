import requests


class Slack:
    def __init__(self, web_token, event_token):
        self.web_token = web_token
        self.event_token = event_token
        self.web = f"https://slack.com/api/"

    def send_message(self, chat, text):
        js = {
            "token": self.web_token,
            "channel": chat,
            "text": text
        }
        requests.post(self.web + "chat.postMessage", data=js)

    def run(self, handle_function=None, debug=False):
        pass
