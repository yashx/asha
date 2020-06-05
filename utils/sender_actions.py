import os
import json
import requests

def inform_user_seen(psid):
    inform_user(psid, "mark_seen")

def inform_user_typing_on(psid):
    inform_user(psid, "typing_on")

def inform_user_typing_off(psid):
    inform_user(psid, "typing_off")

def inform_user(psid, action):
    url_endpoint = "https://graph.facebook.com/v2.6/me/messages"
    params = dict([("access_token", os.getenv("PAGE_TOKEN"))])
    headers = dict([("Content-Type", "application/json")])
    data = json.dumps({
        "recipient":{
            "id":psid
        },
        "sender_action": action
    })
    requests.post(url=url_endpoint, headers=headers, params=params, data=data)