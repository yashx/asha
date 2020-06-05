import os
from flask import Flask, request
import handler

app = Flask(__name__)


@app.route("/", methods=["GET"])
def verify():
    if(request.args.get("hub.mode") == 'subscribe' and request.args.get("hub.challenge")):
        if request.args.get("hub.verify_token") != os.getenv("VERIFY_TOKEN"):
            return "Wrong Token", 403
        return request.args.get("hub.challenge"), 200
    return "Bad request", 400

@app.route("/", methods=["POST"])
def respond():
    data = request.get_json()
    if data.get("object") != "page":
        return "Bad request", 400
    for entry in data.get("entry"):
        for messaging_object in entry.get("messaging"):
            handler.handle_messaging_object(messaging_object)
    return "Okay", 200


if __name__ == "__main__":
    app.run()