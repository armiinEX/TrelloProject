from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_invitation_email(email, board_name, invite_link):
    subject = f"Invitation to join board: {board_name}"
    message = f"You have been invited to join {board_name}.\nClick here to accept: {invite_link}"
    from_email = None  # از DEFAULT_FROM_EMAIL
    send_mail(subject, message, from_email, [email])
