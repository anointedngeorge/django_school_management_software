from mailersend import emails,sms_sending

from decouple import config


def mailsenderApi(
        subject:str, 
        mail_body:dict, 
        mail_from:dict, 
        recipients:dict,
        reply_to:dict, 
    ):

    MAILSENDER_API_KEY = config('MAILSENDER_API_KEY')

    mailer = emails.NewEmail(MAILSENDER_API_KEY)

    mailer.set_mail_from(mail_from, mail_body)
    mailer.set_mail_to(recipients, mail_body)
    mailer.set_subject(subject, mail_body)
    mailer.set_html_content("This is the HTML content", mail_body)
    mailer.set_plaintext_content("Email coming from mailsender...", mail_body)
    mailer.set_reply_to(reply_to, mail_body)
    # using print() will also return status code and data
    return mailer.send(mail_body)



def mailSenderSms(number_from:str, numbers_to:list, message:str):
    MAILSENDER_API_KEY = config('MAILSENDER_API_KEY')
    mailer = sms_sending.NewSmsSending(MAILSENDER_API_KEY)
    # Number belonging to your account in E164 format
    number_from = number_from
    # You can add up to 50 recipient numbers
    numbers_to = numbers_to
    text = message
    obj = mailer.send_sms(number_from, numbers_to, text)
    return obj
