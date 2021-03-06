import json
import requests
from constants import SEND_MESSAGE_URL, PAT as token
from random import randint
import random
import xml.etree.ElementTree
import math

def get_user_info(recipient):
  url_info = "https://graph.facebook.com/v2.6/"+str(recipient)+"?fields=first_name,last_name,profile_pic,locale,timezone,gender&access_token="+str(token)
  r = requests.get(url_info)
  return r.json()
def send_typing_status(recipient):
  """Send the message text to recipient with id recipient.
  """
  r = requests.post(SEND_MESSAGE_URL,
    params={"access_token": token},
      data=json.dumps({
          "recipient": {"id": recipient},
      "sender_action": "typing_on"
    }),
      headers={'Content-type': 'application/json'})
  if r.status_code != requests.codes.ok:
    print r.text

def send_text_message(recipient, text):
  """Send the message text to recipient with id recipient.
  """

  r = requests.post(SEND_MESSAGE_URL,
    params={"access_token": token},
      data=json.dumps({
          "recipient": {"id": recipient},
      "message": {"text": text.decode('unicode_escape')},
    }),
      headers={'Content-type': 'application/json'})
  if r.status_code != requests.codes.ok:
    print r.text

def send_button_template_message(recipient, text, buttons):
    r = requests.post(SEND_MESSAGE_URL,
          params={'access_token': token},
          data=json.dumps({
              "recipient": {"id": recipient},
              "message": {
                  "attachment": {
                  "type": "template",
                  "payload": {
                      "template_type": "button",
                      "text": text,
                      "buttons": buttons
                  }
              }}
          }),
          headers={'Content-type': 'application/json'})
    print r.text

def send_image(recipent, item, type="image"):
    r = requests.post(SEND_MESSAGE_URL, params = {'access_token' : token},
            data = json.dumps({
                "recipient" : {"id" : recipent},
                "message" : {
                    "attachment" : {
                        "type" : type,
                        "payload" : {
                            "url" : item
                        }
                    }
                }
            }),
            headers = {'Content-type' : 'application/json'}
        )
    print r.text

def send_carasol_items(recipient, items):
    r = requests.post(SEND_MESSAGE_URL,
          params={'access_token': token},
          data=json.dumps({
              "recipient": {"id": recipient},
              "message": {"attachment":
                    {
                        "type": "template",
                        "payload": {
                          "template_type": "generic",
                          "elements": items
                      }
                 }    
            }
        }),
        headers={'Content-type': 'application/json'})
    print r.text

def quick_reply(title, payload=None):
    return {
        "content_type" : "text" , 
        "title" : title , 
        "payload" : payload
    }  

def send_replies(recipent , text , reply):
    r = requests.post(SEND_MESSAGE_URL,
          params={'access_token': token},
          data=json.dumps({
              "recipient": {"id": recipent},
              "message": 
                 { 
                 "text" : text,
                 "quick_replies": reply    
                 }    
            
        }),
        headers={'Content-type': 'application/json'})

def generate_carasol_items(text, image_url, payload = None, showbtns = True):
    if showbtns:
        return {
            "title": text,
            "image_url": image_url,
            "buttons": [
                {
                    "type": "postback",
                    "title": "Start Learning",
                    "payload": payload
                },
                {
                    "type": "postback",
                    "title": "Frequently Asked Questions",
                    "payload": payload
                }
            ]
        }
    else:
        return {
            "title": text,
            "image_url": image_url,
        }



def generate_button(text, payload=None, type="text", url=None):
    if type == "url":
        return {
            "type": "web_url",
            "url": url,
            "title": text
        }
    else:
        return {
            "type": "postback",
            "title": text,
            "payload": payload
        }

def get_message(data):
  if data["object"] == "page":

          for entry in data["entry"]:
              for messaging_event in entry["messaging"]:

                  if messaging_event.get("message"):  # someone sent us a message
                      sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                     # recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                      message_text = messaging_event["message"]["text"]  # the message's text
                      return ( message_text , sender_id ) 
#                    send_message(sender_id, "got it, thanks!")

#                if messaging_event.get("delivery"):  # delivery confirmation
#                    pass

#                if messaging_event.get("optin"):  # optin confirmation
#                    pass

#                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
#                    pass

def messaging_events(payload):
    """Generate tuples of (sender_id, message_text) from the
    provided payload.
    """
    data = json.loads(payload)
    messaging_events = data["entry"][0]["messaging"]
    for event in messaging_events:
        if "postback" in event and "payload" in event["postback"]:
            return (event["sender"]["id"], event["postback"]["payload"])
        elif "message" in event and "quick_reply" in event["message"]:
            return (event["sender"]["id"], event["message"]["quick_reply"]["payload"])

def complaint(payload):
    data = json.loads(payload)
    messaging_events = data["entry"][0]["messaging"]
    for event in messaging_events:
       return (event["sender"]["id"], event["message"]["text"])


def urlparser(payload):
    data = json.loads(payload)
    messaging_events = data["entry"][0]["messaging"][0]["message"]["attachments"][0]["payload"]["url"]
    print("url worked")
    messaging_event = data["entry"][0]["messaging"]
    for event in messaging_event:
      return (messaging_events,event["sender"]["id"])

def sendcoordinates(payload):
  data = json.loads(payload)
  messaging_event = data["entry"][0]["messaging"]
  for event in messaging_event:
      sender = event["sender"]["id"]
      return ("Coordinates",sender)

