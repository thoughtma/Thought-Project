# Project Import 
from .models import OurOffices, NewsletterSubscriber

# Third Party Import 
from rest_framework import serializers

# django import
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import re


class OurOfficesSerializer(serializers.ModelSerializer):
    class Meta:
        model = OurOffices
        fields = ['id', 'office_name', 'address', 'contact', 'email']


class NewsletterSubscriberSerializer(serializers.ModelSerializer):

    class Meta:
        model = NewsletterSubscriber
        fields = ['id', 'name', 'email']

    def validate_name(self, value):
        
        if not value.isalpha():
            raise serializers.ValidationError("Name should only contain letters.")
        
        max_length = 30
        if len(value) > max_length:
            raise serializers.ValidationError(f"Name cannot exceed {max_length} characters.")
        
        return value
    

    def validate_email(self, value):
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, value):
            raise serializers.ValidationError("Invalid email address.")
        if not value.endswith('.com'):
            raise serializers.ValidationError("email must have .com domain.")

        return value

 



