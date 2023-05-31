from django import forms
from .models import *

class StudentForm(forms.ModelForm):
    class Meta:
        models = Student
        fields = '__all__'