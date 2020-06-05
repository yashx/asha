import os
import requests

BASE_GRAPH_URL = "https://graph.facebook.com/{}/"

def get_user_first_name(psid):
    """Get first name of user

    Arguments:
        psid {String} -- PSID of user

    Returns:
        String -- first name of user
    """
    return get_user_info_json(psid, "first_name").get("first_name")

def get_user_last_name(psid):
    """Get last name of user

    Arguments:
        psid {String} -- PSID of user

    Returns:
        String -- last name of user
    """
    return get_user_info_json(psid, "last_name").get("last_name")

def get_user_full_name(psid):
    """Get full name of user

    Arguments:
        psid {String} -- PSID of user

    Returns:
        String -- full name of user
    """
    return get_user_info_json(psid, "name").get("name")

def get_user_info_json(psid, fields):
    """Get user info of given field in json

    Arguments:
        psid {String} -- PSID of user
        fields {List/String} -- fields to get

    Returns:
        [Json] -- Json response from user profile api
    """
    if isinstance(fields, str):
        param_value = fields
    else:
        param_value = ",".join(fields)

    response = requests.get(
        BASE_GRAPH_URL.format(psid),
        params=dict(fields=param_value, access_token=os.getenv("PAGE_TOKEN"))
    )

    return response.json()