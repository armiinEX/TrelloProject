from celery import shared_task
from django.core.mail import send_mail
from django.utils.translation import gettext as _
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required


@shared_task
def send_invitation_email(email, board_name, invite_link):
    subject = _("Invitation to join board: %(board_name)s") % {"board_name": board_name}
    message = _("You have been invited to join %(board_name)s.\nClick here to accept: %(invite_link)s") % {
        "board_name": board_name,
        "invite_link": invite_link,
    }
    from_email = None
    send_mail(subject, message, from_email, [email])


@login_required
def invite_test_view(request):
    return render(request, "boards/invite.html")

@login_required
def language_test_view(request):
    return render(request, "boards/language_test.html")