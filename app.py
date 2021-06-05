import requests
import json
from datetime import date
import os
from dotenv import load_dotenv
load_dotenv('.env')

def NotifyToLineChatbot(Reply_message):
    channel_access_token = os.environ.get('Channel_access_token')
    Authorization = "Bearer {}".format(channel_access_token)  
    print(Authorization)

    headers = {
        "Content-Type": "application/json; charset=UTF-8",
        "Authorization": Authorization,
    }

    data = {
        # "to":'Ud67ae8664944cb7d90f2e007051aa720',
        "messages":[{
            "type":"text",
            "text":Reply_message
        }]
    }

    data = json.dumps(data)  ## dump dict >> Json Object
    LINE_API = "https://api.line.me/v2/bot/message/broadcast"
    requests.post(LINE_API, headers=headers, data=data)
if __name__ == "__main__":
    NotifyToLineChatbot('ຕອນນີ້ ph ໃນອ່າງຜັກສູງເກີນໄປ 6.2')
    print('sended')

