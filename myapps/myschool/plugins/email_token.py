import smtplib
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Union, List
from django.conf import settings
from plugins.logging import CreateErrorLog

from plugins.sms_token import Sms80Kobo
# sending email with sendchamp
from sendchamp import Sendchamp
from decouple import config
from authuser.models import *


sendchamp = Sendchamp(public_key=config('SENDCHAMP_BEARER_TOKEN'))
# https://github.com/keosariel/sendchamp-py

import os


smtp = 'mail.gowishway.com'


def to_html(template:str, context:dict):
    from django.template.loader import render_to_string
    from django.conf import settings
    from django.utils import timezone
    try:
        d = os.path.abspath(f"email_template/{template}")
        html_message = render_to_string(template_name=f"email_template/{template}", context=context)
        return html_message
    except Exception as e:
        return f"{e}"






def send_token_via_email(recipient_email):
    try:
        sender_email, sender_password = ('admin@gowishway.com','4=_w}SQ],_#y')
        # Generate a random token
        token = ''.join(random.choices('0123456789128934832100567', k=6))
        # Set up the email message content
        message = f"Your token is: {token}"
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = "Token Verification"
        msg.attach(MIMEText(message, 'plain'))
        # Connect to the email server and send the email message
        server = smtplib.SMTP(smtp, 587)
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, recipient_email, text)
        server.quit()
        return True
    except Exception as e :
        return False 

# Example usage
def check_email_status(recipient_email):
    if send_token_via_email(recipient_email):
        return "Email delivery successfully."
    else:
        return "Email delivery failed."


def sendUserEmail(subject:str, recipient_list:List, context:{}, template:str):

    try:
        sender = {
            "name":settings.EMAIL_HOST_USER,
            "email":settings.EMAIL_HOST_USER
        }
        data, error = sendchamp.email.send(
                    subject=subject,
                    sender=sender,
                    to=recipient_list,
                    message_body={
                        "type": "text/html",
                        "value": to_html(template=f'{template}', context=context )
                    }
                )
        return data, error
    except Exception as e:
        return e



