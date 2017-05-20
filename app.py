import os
import sys
import json
from constants import *
import requests
from flask import Flask, request
from util import *
from mathlib9 import *
import traceback
import random
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient(CONNECTION)
db = client.angelhack10
    

@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200



@app.route('/', methods=['POST'])
def webhook():   
    data = request.json
    print data
    try:
        user = None
        payload = request.get_data()
        sender, message = messaging_events(payload)
        user = db.user.find_one({"fbId": sender})
        if user is None:
            db.user.insert({"fbId": sender, "name": "easy"})
            user = db.user.find_one({"fbId": sender})

        print get_user_info(str(fbId))
        if message == "help":
            send_text_message(sender , "You can choose topic you would like to learn and practice from the menu on left. For more information you can drop us a message and we will reply back to you shortly. ")

        # elif message == "topics_to_learn" or message == "back":
        #     send_text_message(sender , "1.) Operation on Numbers\n2.) Rational Numbers\n3.)Linear Equation in One Variable\n4.)Linear Equations in Two Variables\n5.) Quadratic Equations")
        #     send_replies(
        #         sender, "Enter the number corresponding to the chapter. Example '1' for Operation on Numbers",
        #         [
        #             quick_reply("1",payload="oon"),
        #             quick_reply("2", payload="rat"),
        #             quick_reply("3",payload="lin"),
        #             quick_reply("4",payload="lin2"),
        #             quick_reply("5",payload="quad")
        #         ]) 
        # elif message == "1": 
        #    print "try"
        # elif message == "2": 
        #     send_button_template_message(
        #         sender,
        #         "You have selected the topic, Rational Numbers. What do you want to do next?",
        #         [
        #             generate_button("Learn", "learn" + message),
        #             generate_button("Practice", "prac" + message),
        #             generate_button("Ask Doubts", "ask_doubt" + message)
        #         ]
        #     )
        # elif message == "3": 
        #     send_button_template_message(
        #         sender,
        #         "You have selected the topic, Linear Equation in one variable. What do you want to do next?",
        #         [
        #             generate_button("Learn", "learn" + message),
        #             generate_button("Practice", "prac" + message),
        #             generate_button("Ask Doubts", "ask_doubt" + message)
        #         ]
        #     )
        # elif message == "4": 
        #     send_button_template_message(
        #         sender,
        #         "You have selected the topic, Linear Equation in Two variables. What do you want to do next?",
        #         [
        #             generate_button("Learn", "learn" + message),
        #             generate_button("Practice", "prac" + message),
        #             generate_button("Ask Doubts", "ask_doubt" + message)
        #         ]
        #     )
        # elif message == "5": 
        #     send_button_template_message(
        #         sender,
        #         "You have selected the topic, Quadratic Equations. What do you want to do next?",
        #         [
        #             generate_button("Learn", "learn" + message),
        #             generate_button("Practice", "prac" + message),
        #             generate_button("Ask Doubts", "ask_doubt" + message)
        #         ]
        #     )
    except: 
        pass        
    return "ok"

def log(message):  # simple wrapper for logging to stdout on heroku
    print str(message)
    sys.stdout.flush()


if __name__ == '__main__':
    app.run(debug=True)
