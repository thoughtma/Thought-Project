import sib_api_v3_sdk
from internship_product import settings
from rest_framework import generics, status
from rest_framework.response import Response


def send_mail(email,name):
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = settings.DEFAULT_EMAIL_SENDINBLUE_API
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
    subject = 'Welcome to Our Newsletter'
    message = f"Hi {name},\nThank you for subscribing to our newsletter! We're excited to share the latest news, updates, and courses with you.\nStay tuned for our next newsletter, and in the meantime, feel free to check out our website for more information about our courses and services."

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
        return Response({'error': 'Failed to send email'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        