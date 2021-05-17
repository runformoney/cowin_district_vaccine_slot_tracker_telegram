import requests
from config.config import TELEGRAM_URL, CHAT_ID

def send_message(text):
    params = {'chat_id': -int(CHAT_ID), 'text': text}
    response = requests.post(TELEGRAM_URL, data=params)
    return response


if __name__ == "__main__":
    print(send_message("Test Comment."))