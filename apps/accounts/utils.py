# Python Import
from datetime import date

# Django Import
from django.db import models
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
# from django.utils.encoding import smart_bytes
from django.template.loader import render_to_string
# from django.utils.http import urlsafe_base64_encode
from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.contrib.auth.tokens import PasswordResetTokenGenerator

# Project Import
from apps.student.models import Student
from apps.trainer.models import Trainer
from apps.accounts.models import User
import sib_api_v3_sdk


User = get_user_model()


class Validator:
    def is_valid_user(email, password, request=None):
        try:
            if email is not None:
                obj = User.objects.get(email=email)
                email = obj.email
                user = authenticate(email=email, password=password)
                login(request, user)
            else:
                user = authenticate(email=email, password=password)
                login(request, user)
            if not user:
                return False, "Invalid credentials, please try again.", None
        except Exception as e:
            message = "Invalid credentials"
            return False, message, None
        return True, "success", user.email

    def get_user_instance(email):
        try:
            superuser = User.objects.filter(
                email=email, is_superuser=True, is_staff=True, is_active=True
            ).last()
            student = User.objects.filter(
                email=email, user_type="STUDENT").last()
            trainer = User.objects.filter(
                email=email, user_type="TRAINER").last()

            if superuser:
                user_type = superuser.user_type
                return superuser.id, superuser, user_type
            if student:
                user = User.objects.get(email=email)
                user_type = user.user_type
                return user.id, user.user, user_type
                # user_type = student.user.user_type
                # return student.id, student.user, user_type
            if trainer:
                user_type = trainer.user.user_type
                return trainer.id, trainer.user, user_type

            return False, None
        except Exception as e:
            return False, str(e)


def create_student_user(data, user_type: str) -> User:
    if User.objects.filter(email=data["email"]).exists():
        raise ValueError("This Email already exist.")
    # profile_pic = data.get("profile_pic", None)
    # user = User.objects.create(
    #     email=data["email"], first_name=data["first_name"], last_name=data["last_name"], profile_pic=profile_pic
    # )
    user = User.objects.create(
        email=data["email"], name=data["name"]
    )
    user.set_password(data["password"])
    user.user_type = user_type
    user.username = None
    user.save()

    return user


def create_trainer_user(data, user_type: str) -> User:
    if User.objects.filter(email=data["email"]).exists():
        raise ValueError("This Email already exist.")
    # first_name = data.get("first_name", None)
    # last_name = data.get("last_name", None)
    name = data.get("name", None)
    # profile_pic = data.get("profile_pic", None)
    user = User.objects.create(
        email=data["email"], name=name,
        # profile_pic=profile_pic
    )
    user.set_password(data["password"])
    user.user_type = user_type
    user.username = None
    user.save()
    return user


from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six
class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    """
        Handle Token generation.
        Args:
        Returns:
        """
    def _make_hash_value(self, user, timestamp):
        """
        Generating token for user instance.
        Args:
            :param user: user instance.
            :param timestamp: current timestamp.
        Returns:
            encrypted user token
        """
        return (
                six.text_type(user.pk) + six.text_type(timestamp) + six.text_type(user.is_active)
        )
account_activation_token = AccountActivationTokenGenerator()



def send_student_credential(email , name, password):
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = settings.DEFAULT_EMAIL_SENDINBLUE_API
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

    subject = 'Your Login Credentials'
    message = f'Hi {name},\n\nYour account has been created.\n\nEmail: {email}\nPassword: {password}\n\nThank you for registering!'

    html_content = f'<html><body><h1>{message}</h1></body></html>'

    sender = {"email": settings.DEFAULT_EMAIL_SENDER, "name": settings.DEFAULT_EMAIL_SENDER_NAME}
    to = [{"email": email}]
    reply_to = {"email": settings.DEFAULT_EMAIL_SENDER, "name": settings.DEFAULT_EMAIL_SENDER_NAME}
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=to, reply_to=reply_to, html_content=html_content, sender=sender, subject=subject)

    try:
        api_response = api_instance.send_transac_email(send_smtp_email)
        print(api_response)
    except sib_api_v3_sdk.ApiException as e:
        print("Exception when sending email to user:", email)




def send_trainer_credential(email , name, password):

    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = settings.DEFAULT_EMAIL_SENDINBLUE_API
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

    subject = 'Your Login Credentials'
    message = f'Hi {name},\n\nYour account has been created.\n\nEmail: {email}\nPassword: {password}\n\nThank you for registering!'

    html_content = f'<html><body><h1>{message}</h1></body></html>'

    sender = {"email": settings.DEFAULT_EMAIL_SENDER, "name": settings.DEFAULT_EMAIL_SENDER_NAME}
    to = [{"email": email}]
    reply_to = {"email": settings.DEFAULT_EMAIL_SENDER, "name": settings.DEFAULT_EMAIL_SENDER_NAME}
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=to, reply_to=reply_to, html_content=html_content, sender=sender, subject=subject)

    try:
        api_response = api_instance.send_transac_email(send_smtp_email)
        print(api_response)
    except sib_api_v3_sdk.ApiException as e:
        print("Exception when sending email to user:", email)


