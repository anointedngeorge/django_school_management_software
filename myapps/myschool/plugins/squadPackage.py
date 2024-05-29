
import re
import string
import uuid
from decouple import config
import requests as req


class Squad:
    
    def __init__(self) -> None:
        self.SQUAD_TRANSACTION_INITIATE = config("SQUAD_TRANSACTION_INITIATE")
        self.SQUAD_PAYMENT_VERIFY = config("SQUAD_PAYMENT_VERIFY")
        self.SQUAD_CALLBACK_URL = config("SQUAD_CALLBACK_URL")
        self.SQUAD_TRANSFER_URL = config("SQUAD_TRANSFER_URL")
        self.SQUAD_AUTHENTICATION_BEARER = config("SQUAD_AUTHENTICATION_BEARER")


    def initiate(self, amount:int, email:str, currency:str):
        ref =  uuid.uuid4().hex
        data = {}
        data['amount'] = amount
        data['email'] = email
        data['currency'] = currency
        data['initiate_type'] = "inline"
        data['transaction_ref'] = f"{ref}"
        data['callback_url'] = self.SQUAD_CALLBACK_URL

        # try:
        #     header_content = {
        #         'headers': {
        #             "Content-Type":"application/json",
        #             "Authentication":f"Bearer {self.SQUAD_AUTHENTICATION_BEARER}"
        #         }
        #     }
        #     rq = req.post(
        #         url=self.SQUAD_TRANSACTION_INITIATE,
        #         headers=header_content
        #     )

        #     response =  rq.json()
        #     print(response)
        # except Exception as e:
        #     pass


        return ref

    
    def verify(self):
        pass

    def transfer(self):
        pass
        
Squad()