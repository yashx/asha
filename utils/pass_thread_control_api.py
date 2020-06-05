import os
import json
import requests

BASE_URL = "https://graph.facebook.com/v2.6/me/pass_thread_control"

def pass_thread_control(psid, metadata, target_app_id=None):
    """method to pass thread control.
    Specify the app id otherwise default will be used

    Args:
        psid (String): PSID of user
        metadata (String): metadata to send
        target_app_id (String, optional): Target app id. Defaults to None.

    Returns:
        Integer: status code indicating if it was successful or not
    """
    if target_app_id is None:
        target_app_id = os.getenv("HIDDEN_MAIL_ID")

    param = {"access_token": os.getenv("PAGE_TOKEN")}

    header = {"Content-Type": "application/json"}

    post_data = json.dumps({
        "recipient":{"id":psid},
        "target_app_id":int(target_app_id),
        "metadata":metadata
    })

    return requests.post(BASE_URL, params=param, headers=header, data=post_data).status_code
