# Django Import
from django.utils.encoding import force_str
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import PasswordResetTokenGenerator

# Project Import
from apps.accounts import utils

# Third Party Import
from rest_framework import serializers


User = get_user_model()


class UserLoginSerializer(serializers.Serializer):
    id = serializers.CharField(required=False)
    email = serializers.EmailField()
    name = serializers.EmailField(required=False)
    password = serializers.CharField()
    tokens = serializers.CharField(read_only=True)
    refresh_token = serializers.CharField(read_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if not email:
            raise serializers.ValidationError('Email is required')

        if not password:
            raise serializers.ValidationError('Password is required')

        try:
            user = authenticate(username=email, password=password)
        except Exception:
            raise serializers.ValidationError(
                'Error occurred while logging in')

        if not user:
            raise serializers.ValidationError('Incorrect email or password')

        if not user.is_active:
            raise serializers.ValidationError('User account is inactive')

        data['user'] = user
        return {
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "tokens": user.tokens().get("access"),
            "refresh_token": user.tokens().get("refresh"),
            "password": user.password,
        }


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    def validate(self, validated_data):
        request = self.context.get('request')
        password = validated_data.get('new_password')
        confirm_password = validated_data.get('confirm_password')
        old_password = validated_data.get('old_password')
        if not request.user.check_password(old_password):
            raise Exception("Old Password Does Not Match!")
        if password != confirm_password:
            raise Exception("Password does not match.")
        if len(password) < 5:
            raise Exception("The password must be at least 8 characters.")
        return validated_data


class UpdateUserIsActiveStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['is_active']



class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
