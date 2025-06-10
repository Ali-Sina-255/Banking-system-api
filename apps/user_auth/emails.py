from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.translation import gettext_lazy as _
from loguru import logger


def send_otp_email(email, opt):
    subject = _("Your OTP code for login.")
    from_email = settings.DEFAULT_EMAIL
    recipient_list = [email]

    context = {
        "otp": opt,
        "expiry_time": settings.OPT_EXPIRATION,
        "site_name": settings.SITE_NAME,
    }
    html_email = render_to_string("emails/opt_email.html", context)
    plain_email = strip_tags(html_email)
    email = EmailMultiAlternatives(subject, plain_email, from_email, recipient_list)
    email.attach_alternative(html_email, "text/html")
    try:
        email.send()
        logger.success(f"OTP email send successfully to : {email}")
    except Exception as e:
        logger.error(f"Failed to send OTP email {email}: Error: {str(e)} ")


def send_account_locked_email(self):
    subject = _("Your Account had been locked")
    from_email = settings.DEFAULT_EMAIL
    recipient_list = [self.email]

    context = {
        "user": self,
        "logout_duration": int(settings.LOCKOUT_DURATION.total_second() // 60),
        "site_name": settings.SITE_NAME,
    }
    html_email = render_to_string("emails/account_locked.html", context)
    plain_email = strip_tags(html_email)
    email = EmailMultiAlternatives(subject, plain_email, from_email, recipient_list)
    email.attach_alternative(html_email, "text/html")
    try:
        email.send()
        logger.success(f"Account locked email send to : {self.email}")
    except Exception as e:
        logger.error(
            f"Failed to send acount locked email to {self.email}: Error: {str(e)} "
        )
