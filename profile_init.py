import os
import json
import requests
import constant

# TODO
# Add more hindi locale
# set persistent menu

BASE_PROFILE_API_URL = "https://graph.facebook.com/v7.0/me/messenger_profile"


def init():
    params = dict([("access_token", os.getenv("PAGE_TOKEN"))])
    headers = dict([("Content-Type", "application/json")])
    data = json.dumps({
        "get_started":{
            "payload":constant.payload.GET_STARTED_PAYLOAD
        },
        "greeting":[
            {
                "locale":"default",
                "text":constant.message.GREETING
            }
        ],
        "persistent_menu": [
            {
                "locale": "default",
                "call_to_actions": [
                    {
                        "type": "postback",
                        "title": constant.message.TELL_JOKE,
                        "payload": constant.payload.TELL_A_JOKE
                    }
                ]
            }
        ]
    })

    resp = requests.post(BASE_PROFILE_API_URL, params=params, headers=headers, data=data)
    print(resp)

def get_set_values():
    params = dict(access_token=os.getenv("PAGE_TOKEN"), fields=r"whitelisted_domains,greeting")
    resp = requests.get(BASE_PROFILE_API_URL, params=params)
    print(resp.text)

if __name__ == "__main__":
    init()
    # get_set_values()