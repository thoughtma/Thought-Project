# Django Imports
from django.shortcuts import render
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from internship_product import settings

# Third Party Import
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.response import Response
import sib_api_v3_sdk

# Project Import
from apps.accounts import create_response_util
from apps.accounts.utils import account_activation_token
from apps.accounts.serializers import (
    UserLoginSerializer, ChangePasswordSerializer, ForgotPasswordSerializer)

User = get_user_model()


class UserLoginApi(APIView):
    serializer_class = UserLoginSerializer

    def post(self, request):
        """
        API endpoint to log in a user.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            A JSON response containing the status of the request and any relevant data or errors.

        Raises:
            N/A
        """
        try:
            data = request.data
            serializer = self.serializer_class(
                data=data, context={'request': request})
            if serializer.is_valid():
                return create_response_util.create_response_data(
                    message="success",
                    status=status.HTTP_200_OK,
                    data=serializer.data,
                    errors=None,
                )
            else:
                return create_response_util.create_response_data(
                    message="failed",
                    status=status.HTTP_400_BAD_REQUEST,
                    data=None,
                    errors=serializer.errors,
                )

        except Exception as e:
            return create_response_util.create_response_data(
                message="failed",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                data=None,
                errors=str(e),
            )


class ChangePassword(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        """
        Retrieve the current user object.

        Returns:
            The current user object.

        """
        obj = self.request.user
        return obj

    def put(self, request, *args, **kwargs):
        """
        Handle the PUT request to change the user's password.

        Args:
            request: The request object.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            A response object indicating the success or failure of the password change.

        """
        try:
            self.object = self.get_object()
            serializer = self.serializer_class(
                data=request.data, context={'request': request})
            if serializer.is_valid():
                self.object.set_password(serializer.data.get("new_password"))
                self.object.save()
                return create_response_util.create_response_data(
                    message="success",
                    status=status.HTTP_200_OK,
                    data=None,
                    errors=None,
                )
            else:
                return create_response_util.create_response_data(
                    message="failed",
                    status=status.HTTP_400_BAD_REQUEST,
                    data=None,
                    errors=serializer.errors,
                )
        except Exception as e:
            return create_response_util.create_response_data(
                message="failed",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                data=None,
                errors=str(e),
            )


class ForgotPasswordView(generics.GenericAPIView):
    serializer_class = ForgotPasswordSerializer

    def post(self, request):
        """
        A view that sends a password reset link to the user's email address.

        Required POST Parameters:
            - email (string): The email address of the user who wants to reset their password.

        Returns:
            - 200 OK: If the email was sent successfully.
            - 400 BAD REQUEST: If the input parameters are invalid.
            - 500 INTERNAL SERVER ERROR: If there was an error while sending the email.

        Raises:
            - ValidationError: If the email address is not found in the database.
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        instance = User.objects.filter(email=email).first()
        if instance is None:
            return create_response_util.create_response_data(
                    message="failed",
                    status=status.HTTP_400_BAD_REQUEST,
                    data=None,
                    errors="Invalid email address",
                )
        configuration = sib_api_v3_sdk.Configuration()
        configuration.api_key['api-key'] = settings.DEFAULT_EMAIL_SENDINBLUE_API
        api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

        user_id = urlsafe_base64_encode(force_bytes(instance.id))
        token = account_activation_token.make_token(instance)
        confirmation_link = f"https://graduate.thoughtwin.com/reset-password/{user_id}/"

        subject = 'Verification and password-set mail'
        message = f"Hi {instance.email},\nThis is the mail regarding your Forget Password request from Intenship Product by Thoughtwin Portal.\nPlease click on this link to reset the account password.\n{confirmation_link}"

        html_content = f'<html><body><h1>{message}</h1></body></html>'

        sender = {"email": settings.DEFAULT_EMAIL_SENDER, "name": settings.DEFAULT_EMAIL_SENDER_NAME}
        to = [{"email": instance.email}]
        reply_to = {"email": settings.DEFAULT_EMAIL_SENDER, "name": settings.DEFAULT_EMAIL_SENDER_NAME}
        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=to, reply_to=reply_to, html_content=html_content, sender=sender, subject=subject)

        try:
            api_response = api_instance.send_transac_email(send_smtp_email)
            print(api_response)
        except sib_api_v3_sdk.ApiException as e:
            print("Exception when sending email to user:", instance.email)
            return Response({'error': 'Failed to send email'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return create_response_util.create_response_data(
                    message="A password reset link has been sent to your email address.", 
                    status=status.HTTP_200_OK, 
                    data=None, errors=None
                )
        


class ResetPasswordView(generics.GenericAPIView):
    """
    API view for resetting user password.
    Accepts a POST request with the following parameters:
    - uid: user ID encoded in base 64
    - token: token generated for user password reset
    - password: new password to set
    - confirm_password: new password confirmation
    Returns a response with a success or error message.
    """
    def post(self, request, token):
        uid = force_str(urlsafe_base64_decode(token))
        user = User.objects.filter(pk=uid).first()
        if user is None:
            # return Response({'error': 'Invalid reset link'}, status=status.HTTP_400_BAD_REQUEST)
            return create_response_util.create_response_data(
                    message="failed",
                    status=status.HTTP_400_BAD_REQUEST,
                    data=None,
                    errors="Invalid reset link",
                )
        password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_password')
        if password != confirm_password:

            return create_response_util.create_response_data(
                    message="failed",
                    status=status.HTTP_400_BAD_REQUEST,
                    data=None,
                    errors="Passwords do not match",
                )
        
        user.set_password(password)
        user.save()
        
        return create_response_util.create_response_data(
                    message="Your password has been successfully changed.", 
                    status=status.HTTP_200_OK, 
                    data=None, errors=None
                    )