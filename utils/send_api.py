import os
import json
import requests

SEND_API_URL = "https://graph.facebook.com/v7.0/me/messages"
PARAMS = dict([("access_token", os.getenv("PAGE_TOKEN"))])
HEADERS = dict([("Content-Type", "application/json")])

def data_former_from_dict(psid, message):
    return json.dumps({
        "recipient":{
            "id":psid
        },
        "message":message,
        "messaging_type": "RESPONSE"
    })

def send_simple_message(psid, text_message):
    """Send a simple message

    Arguments:
        psid {String} -- PSID of user
        text_message {String} -- text message to send
    """
    data = data_former_from_dict(psid, dict(text=text_message))
    requests.post(SEND_API_URL, params=PARAMS, headers=HEADERS, data=data)

def send_text_with_quick_reply(psid, text_message, options):
    """send a text message with text quick reply options

    Arguments:
        psid {String} -- PSID of user
        text_message {String} -- text message to send
        options {Dictionary} -- dictionary with text option and payload as key value pairs
    """
    quick_replies = []
    for key, value in options.items():
        quick_replies.append({
            "content_type":"text",
            "title":key,
            "payload":value,
        })

    data = data_former_from_dict(psid, dict(text=text_message, quick_replies=quick_replies))
    requests.post(SEND_API_URL, params=PARAMS, headers=HEADERS, data=data)

def send_text_with_url_button(psid, text_message, options):
    """Send a button template with url button

    Arguments:
        psid {String} -- PSID of user
        text_message {String} -- Text that appears above button
        options {Dictionary} -- dictionary with text label and url as key value pairs
    """

    buttons = []

    for key, value in options.items():
        buttons.append({
                        "type": "web_url",
                        "url": value,
                        "title": key
                        })

    message = {
        "attachment":{
            "type":"template",
            "payload":{
                "template_type":"button",
                "text":text_message,
                "buttons": buttons
            }
        }
    }

    data = data_former_from_dict(psid, message)


    requests.post(SEND_API_URL, params=PARAMS, headers=HEADERS, data=data)