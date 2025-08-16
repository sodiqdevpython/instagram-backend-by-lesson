from threading import Thread
import requests
from decouple import config
from django.core.mail import send_mail

def send_verify_code_mail(subject, message, from_email, recipient_list, html_message=None):
    thread = Thread(
        target=send_mail,
        args=(subject, message, from_email, recipient_list),
        kwargs={'html_message': html_message}
    )
    thread.start()

def SmsMessage(to, from_, text):
    url = "https://messages-sandbox.nexmo.com/v1/messages"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    auth = (config("VONAGE_KEY"), config("VONAGE_API_SECRET"))
    payload = {
        "from": from_,
        "to": to,
        "message_type": "text",
        "text": text,
        "channel": "whatsapp"
    }
    response = requests.post(url, headers=headers, auth=auth, json=payload)
    print("Status:", response.status_code)
    print("Response:", response.json())
    return response.json()

def send_verify_code_sms(code, phone_number):
    return SmsMessage(
        to=f"998{phone_number}",
        from_=config("VONAGE_PHONE_NUMBER"),
        text=f"Sizning tasdiqlash parolingiz: {code}"
    )


def send_verify_code_sms_thread(code, phone_number):
    thread = Thread(target=send_verify_code_sms, args=(code, phone_number))
    thread.start()