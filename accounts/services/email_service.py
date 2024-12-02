from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.translation import gettext as _


class EmailService:
    @staticmethod
    def send_activation_email(
        username: str, domain: str, to_email: str, uid: str, token: str
    ) -> None:
        mail_subject = _("Activation link has been sent to your email")
        from_email = settings.EMAIL_HOST_USER

        context = {
            "username": username,
            "domain": domain,
            "uid": uid,
            "token": token,
        }

        message = render_to_string("accounts/account_activation_email.html", context)
        send_mail(mail_subject, message, from_email, [to_email], html_message=message)
