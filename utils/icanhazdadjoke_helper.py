import random
import requests
import constant

BASE_URL = "https://icanhazdadjoke.com/"
HEADERS = dict(Accept="text/plain")
def get_a_joke():
    try:
        resp = requests.get(BASE_URL, headers=HEADERS, timeout=2)
        if resp.status_code != 200:
            return random.choice(constant.default_jokes)
        return resp.text
    except Exception:
        return random.choice(constant.default_jokes)
