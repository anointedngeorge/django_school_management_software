from fcm_django.models import FCMDevice
import firebase_admin
from firebase_admin import credentials, messaging

cred = credentials.Certificate("plugins/keen-tokenizer-400311-firebase-adminsdk-yhti1-fbad4dfa56.json")
firebase_admin.initialize_app(cred)


def sendPush(title='', message='', registration_token='', data=None):
    try:
        message = messaging.MulticastMessage(
            notification=messaging.Notification(
                title=title,
                body=message
            ),
            data=data,
            tokens=registration_token
        )
        response = messaging.send_multicast(message)
        return response
    except Exception as e:
        return str(e)
    

