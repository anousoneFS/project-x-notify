import requests
import json
from datetime import date
# import os
# from dotenv import load_dotenv
# load_dotenv('.env')

#old asscess token
#Channel_access_token = 'MzDOjvnMWXtqfZFpmsf9wRC43cPRyZaSMm7sTrNw/azWCpe5baR6FF3JZM5MhNCdsTwcZBWvxrVGazB7KFhCJdCa7km/RB7ptoCcFM8iZSdwZ+V3ZNK/Z+qOkSxTuOfH95Bl5Y9zf61MGJs8fYf2yQdB04t89/1O/w1cDnyilFU='

channel_access_token = 'AB8POin6mVb9bv/wGRXUzz+B+5Uckd5GzmkEewyVrTT3D3IvSErCKgQ5I/Z2teyCbs/+ASy+TgxCIs8oDf5c4VkB7pedx9DdY6qKy+5QiPAyTCWC1RInHmg4ExKGfxaDCefMCreOrHaKLDev/jX9+gdB04t89/1O/w1cDnyilFU='
def NotifyToLineChatbot(Reply_message):
    # channel_access_token = os.environ.get('Channel_access_token')
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
    NotifyToLineChatbot('ຍິນດີຕ້ອນຮັບເຂົ້າສູ່ project-x farm')
    print('sended')

