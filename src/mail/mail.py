from flask_mail import Message
from main import mail
from models.models import *

def send_email(recipient_email, subject, body):
    msg = Message(subject, recipients=[recipient_email])
    msg.body = body
    try:
        mail.send(msg)
        return True
    except Exception as e:
        print(f'Failed to send email: {e}')
        return False


