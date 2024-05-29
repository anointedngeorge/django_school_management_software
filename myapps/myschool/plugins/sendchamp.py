import requests
from decouple import config
import json


def sendChampEmail(
        message_body:str, 
        subject:str,
        recipient:list,
        sender:dict,
    ):

    try:
        url = f"{config('SENDCHAMP_URI')}/email/send"
        token =  config('SENDCHAMP_BEARER_TOKEN')

        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "Authorization":f"Bearer {token}"
        }

        payload = {
            "subject":subject,

            "to":recipient,

            "from":sender,

            "message_body":{
                "type":"text/html",
                "value":message_body
            }
        }
        response = requests.post(url, headers=headers, json=payload )
        return response
    
    except Exception as e:
        return f"{e}"
    




