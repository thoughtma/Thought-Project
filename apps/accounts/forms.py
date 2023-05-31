from django import forms
from .models import *

class CustomeUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'
