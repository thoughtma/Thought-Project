# Django Import
from django import forms
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.core.validators import RegexValidator

# Project Import
from apps.student.models import *
from apps.accounts.models import *
from apps.courses.models import Courses, WhatYouLearn, AboutCourse, CareerPath, Syllabus, SubSyllabus
from apps.trainer.models import Trainer,LectureVideo,Queries, ReplyThread

class StudentForm(forms.ModelForm):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    contact = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())
    enrolled_course = forms.ModelMultipleChoiceField(
        queryset=Courses.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'})
    )
    username = forms.CharField(max_length=100)

    # Define regex patterns for validation
    name_regex = r'^[A-Za-z\s]+$'
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$'
    contact_regex = r'^\d{10}$'

    # Apply regex validations using RegexValidator
    name_validator = RegexValidator(
        regex=name_regex,
        message='Name can only contain alphabets and spaces.'
    )
    email_validator = RegexValidator(
        regex=email_regex,
        message='Invalid email format.'
    )
    contact_validator = RegexValidator(
        regex=contact_regex,
        message='Contact number must be a 10-digit number.'
    )


    class Meta:
        model = Student
        fields = [
            'name',
            'email',
            'contact',
            'password' ,
            'highest_qualification',
            'category',
            'username',
            'enrolled_course'
            ]

    widgets = {
            'name': forms.Select(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'contact': forms.TextInput(attrs={'class': 'form-control'}),
            'highest_qualification': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.TextInput(attrs={'class': 'form-control'}),
            'enrolled_course': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].validators.append(self.name_validator)
        self.fields['email'].validators.append(self.email_validator)
        self.fields['contact'].validators.append(self.contact_validator)


class UserForm(forms.ModelForm):
    # content_type_student = ContentType.objects.get(app_label='student', model='student')
    # content_type_trainer = ContentType.objects.get(app_label='trainer', model='trainer')
    # content_type_courses = ContentType.objects.get(app_label='courses', model='courses')
    # content_type_enquirers_forms = ContentType.objects.get(app_label='student', model='enquirersforms')
    # content_type_queries = ContentType.objects.get(app_label='trainer', model='queries')
    # content_type_student_reviews = ContentType.objects.get(app_label='student', model='studentreviews')

    # permissions = forms.ModelMultipleChoiceField(
    #     queryset=Permission.objects.filter(content_type__in=[
    #         content_type_student, content_type_trainer, content_type_courses,
    #         content_type_enquirers_forms, content_type_queries,
    #         content_type_student_reviews
    #     ]),
    #     widget=forms.CheckboxSelectMultiple,
    #     required=False
    # )

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['permissions'].choices = [
    #         (permission.id, self.get_permission_label(permission))
    #         for permission in self.fields['permissions'].queryset
    #     ]

    # def get_permission_label(self, permission):
    #     if permission.content_type == self.content_type_student:
    #         if permission.codename == 'add_student':
    #             return "Add Student"
    #         elif permission.codename == 'change_student':
    #             return "Update Student"
    #         elif permission.codename == 'delete_student':
    #             return "Delete Student"
    #         elif permission.codename == 'view_student':
    #             return "View Student"

    #     elif permission.content_type == self.content_type_trainer:
    #         if permission.codename == 'add_trainer':
    #             return "Add Trainer"
    #         elif permission.codename == 'change_trainer':
    #             return "Update Trainer"
    #         elif permission.codename == 'delete_trainer':
    #             return "Delete Trainer"
    #         elif permission.codename == 'view_trainer':
    #             return "View Trainer"

    #     elif permission.content_type == self.content_type_courses:
    #         if permission.codename == 'add_courses':
    #             return "Add Courses"
    #         elif permission.codename == 'change_courses':
    #             return "Update Courses"
    #         elif permission.codename == 'delete_courses':
    #             return "Delete Courses"
    #         elif permission.codename == 'view_courses':
    #             return "View Courses"

    #     elif permission.content_type == self.content_type_enquirers_forms:
    #         if permission.codename == 'add_enquirersforms':
    #             return "Add Enquiry Forms"
    #         elif permission.codename == 'change_enquirersforms':
    #             return "Update Enquiry Forms"
    #         elif permission.codename == 'delete_enquirersforms':
    #             return "Delete Enquiry Forms"
    #         elif permission.codename == 'view_enquirersforms':
    #             return "View Enquiry Forms"

    #     elif permission.content_type == self.content_type_queries:
    #         if permission.codename == 'add_queries':
    #             return "Add Queries"
    #         elif permission.codename == 'change_queries':
    #             return "Update Queries"
    #         elif permission.codename == 'delete_queries':
    #             return "Delete Queries"
    #         elif permission.codename == 'view_queries':
    #             return "View Queries"

    #     elif permission.content_type == self.content_type_student_reviews:
    #         if permission.codename == 'add_studentreviews':
    #             return "Add Student Reviews"
    #         elif permission.codename == 'change_studentreviews':
    #             return "Update Student Reviews"
    #         elif permission.codename == 'delete_studentreviews':
    #             return "Delete Student Reviews"
    #         elif permission.codename == 'view_studentreviews':
    #             return "View Student Reviews"

    #     else:
    #         return str(permission)

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     permissions = list(self.fields['permissions'].queryset)
    #     permissions.sort(key=self.get_permission_order)
    #     self.fields['permissions'].choices = [
    #         (permission.id, self.get_permission_label(permission))
    #         for permission in permissions
    #     ]

    # def get_permission_order(self, permission):
    #     if permission.content_type == self.content_type_student:
    #         return 1
    #     elif permission.content_type == self.content_type_trainer:
    #         return 2
    #     elif permission.content_type == self.content_type_courses:
    #         return 3
    #     elif permission.content_type == self.content_type_enquirers_forms:
    #         return 4
    #     elif permission.content_type == self.content_type_queries:
    #         return 5
    #     elif permission.content_type == self.content_type_student_reviews:
    #         return 6
    #     else:
    #         return 7

    name = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        validators=[
            RegexValidator(
                regex=r'^[A-Za-z\s]+$',
                message='Name can only contain alphabets and spaces.'
            )
        ]
    )
    email = forms.EmailField(
        max_length=90,
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$',
                message='Invalid email format.'
            )
        ]
    )
    contact = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        validators=[
            RegexValidator(
                regex=r'^\d{10}$',
                message='Contact number must be a 10-digit number.'
            )
        ]
    )
    class Meta:
        model = User
        fields = [
            'email',
            'name',
            # 'user_type',
            'contact',
            # 'permissions',
            'password',
            'designation',
            ]

class UserUpdateForm(forms.ModelForm):

    name = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        validators=[
            RegexValidator(
                regex=r'^[A-Za-z\s]+$',
                message='Name can only contain alphabets and spaces.'
            )
        ]
    )
    email = forms.EmailField(
        max_length=90,
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$',
                message='Invalid email format.'
            )
        ]
    )
    contact = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        validators=[
            RegexValidator(
                regex=r'^\d{10}$',
                message='Contact number must be a 10-digit number.'
            )
        ]
    )
    class Meta:
        model = User
        fields = [
            'email',
            'name',
            'contact',
            'designation',
            ]

class CourseForm(forms.ModelForm):
    class Meta:
        model = Courses
        fields = ['course_name','title', 'description', 'rating', 'students_enrolled','job_guarantee','online_classes','offline_classes','duration','skills','start_date','language','category','course_image']

class WhatYouLearnForm(forms.ModelForm):
    class Meta:
        model = WhatYouLearn
        fields = ['course_name', 'whatyoulearn_description']

class AboutCourseForm(forms.ModelForm):
    class Meta:
        model = AboutCourse
        fields = ['course_name', 'aboutcourse_description', 'about_course_image']

class CareerPathForm(forms.ModelForm):
    class Meta:
        model = CareerPath
        fields = ['course_name', 'career_path_description', 'career_path_image']

class SyllabusForm(forms.ModelForm):
    class Meta:
        model = Syllabus
        fields = ['course_name', 'chapter', 'chapter_description', 'syllabus_image' ]

class SubSyllabusForm(forms.ModelForm):
    class Meta:
        model = SubSyllabus
        fields = ['syllabus', 'sub_chapter', 'subchapter_description', 'sub_syllabus_image' ]


#r_k

class TrainerForm(forms.ModelForm):

    class Meta:
        model = Trainer
        fields = [
            'name',
            'email',
            'contact',
            'specialization',
            'experience',
            'address'
        ]

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['name'].required = True
            self.fields['email'].required = True
            self.fields['contact'].required = True

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'required': False}),
            'contact': forms.NumberInput(attrs={'class': 'form-control'}),
            'specialization': forms.Select(attrs={'class': 'form-control'}),
            'experience': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.DateInput(attrs={'class': 'form-control'}),
        }

        
  





class UpdateTrainerForm(forms.ModelForm):
    name = forms.CharField(max_length=30, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    email = forms.EmailField(max_length=30, widget=forms.EmailInput(
        attrs={'class': 'form-control'}))
    contact = forms.CharField(max_length=30, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    
    # Define regex patterns for validation
    name_regex = r'^[A-Za-z\s]+$'
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$'
    contact_regex = r'^\d{10}$'

    # Apply regex validations using RegexValidator
    name_validator = RegexValidator(
        regex=name_regex,
        message='Name can only contain alphabets and spaces.'
    )
    email_validator = RegexValidator(
        regex=email_regex,
        message='Invalid email format.'
    )
    contact_validator = RegexValidator(
        regex=contact_regex,
        message='Contact number must be a 10-digit number.'
    )

    class Meta:
        model = Trainer
        fields = ('name', 'email',
                  'contact', 'specialization',
                  'experience', 'address'
                  )

        widgets = {
            'specialization': forms.Select(attrs={'class': 'form-control'}),
            'experience': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
        }

    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['specialization'].required = True
        self.fields['experience'].required = True
        self.fields['address'].required = True
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].validators.append(self.name_validator)
        self.fields['email'].validators.append(self.email_validator)
        self.fields['contact'].validators.append(self.contact_validator)

    def save(self, commit=True):
        trainer = super().save(commit=False)
        trainer.name = self.cleaned_data['name']
        trainer.email = self.cleaned_data['email']
        trainer.contact = self.cleaned_data['contact']
        trainer.specialization = self.cleaned_data['specialization']
        trainer.experience = self.cleaned_data['experience']
        trainer.address = self.cleaned_data['address']
        trainer.save()
        trainer = super(self.__class__, self).save(commit=False)
        trainer = trainer
        if commit:
            trainer.save()
        return trainer


class LectureVideoForm(forms.ModelForm):
    class Meta:
        model = LectureVideo
        fields = ['course', 'trainer',
                  'syllabus', 'title',
                  'lecture_video'
                  ]

        widgets = {
            'course': forms.Select(attrs={'class': 'form-control'}),
            # 'contact': forms.TextInput(attrs={'class': 'form-control'}),
            'trainer': forms.Select(attrs={'class': 'form-control'}),
            'syllabus': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'lecture_video': forms.FileInput(attrs={'class': 'form-control'}),

        }


class ContactUsForm(forms.ModelForm):

    class Meta:
        model = ContactForms
        fields = ('name', 'contact', 'email', 'address', 'message',)

        widgets = {
            'name': forms.Select(attrs={'class': 'form-control'}),
            'contact': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'message': forms.TextInput(attrs={'class': 'form-control'}),
        }


class EnquiryForm(forms.ModelForm):

    class Meta:
        model = EnquirersForms
        fields = ('name', 'mobile_number', 'email', 'highest_qualification', 'category', 'comment', 'priority')

        widgets = {
            'name': forms.Select(attrs={'class': 'form-control'}),
            'mobile_number': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'highest_qualification': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.TextInput(attrs={'class': 'form-control'}),
            'comment': forms.TextInput(attrs={'class': 'form-control'}),
            'priority': forms.TextInput(attrs={'class': 'form-control'}),
        }


class StudentReviewForm(forms.ModelForm):

    class Meta:
        model = StudentReviews
        fields = ('student', 'course', 'rating', 'comment',)

        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'course': forms.TextInput(attrs={'class': 'form-control'}),
            'rating': forms.EmailInput(attrs={'class': 'form-control'}),
            'comment': forms.TextInput(attrs={'class': 'form-control'}),
        }


# Quries Form
# class QuiresForm(forms.ModelForm):
#     class Meta:

#         model = Queries
#         fields = ['student','syllabus',
#                 'query_headline','query',
#                 'response', 'response_by']

#         widgets = {
#             'student': forms.Select(attrs={'class': 'form-control'}),
#             'syllabus': forms.Select(attrs={'class': 'form-control'}),
#             'query_headline': forms.TextInput(attrs={'class': 'form-control'}),
#             'query': forms.TextInput(attrs={'class': 'form-control'}),
#             'response': forms.TextInput(attrs={'class': 'form-control'}),
#             'response_by': forms.Select(attrs={'class': 'form-control'}),

#         }


class QueryThreadForm(forms.ModelForm):
    class Meta:
        model = ReplyThread
        fields = ['response','response_by']  # Include only the 'response' field in the form

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['response'].required = True  # Set the 'response' field as required


class StudentUpdateForm(forms.ModelForm):
    name = forms.CharField(max_length=30, widget=forms.EmailInput(
        attrs={'class': 'form-control'}))
    email = forms.EmailField(max_length=30, widget=forms.EmailInput(
        attrs={'class': 'form-control'}))
    contact = forms.CharField(max_length=30, widget=forms.EmailInput(
        attrs={'class': 'form-control'}))
    

    # Define regex patterns for validation
    name_regex = r'^[A-Za-z\s]+$'
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$'
    contact_regex = r'^\d{10}$'

    # Apply regex validations using RegexValidator
    name_validator = RegexValidator(
        regex=name_regex,
        message='Name can only contain alphabets and spaces.'
    )
    email_validator = RegexValidator(
        regex=email_regex,
        message='Invalid email format.'
    )
    contact_validator = RegexValidator(
        regex=contact_regex,
        message='Contact number must be a 10-digit number.'
    )

    class Meta:
        model = Student
        fields = (
            'name',
            'email',
            'contact', 
            'highest_qualification',
            'category', 
            'local_address',
            # 'permanent_address', 
            'father_name',
            'father_mobile_number',
            'enrolled_course'
                  )

        # widgets = {
        #     'highest_qualification': forms.TextInput(attrs={'class': 'form-control'}),
        #     'category': forms.Select(attrs={'class': 'form-control'}),
        #     'local_address': forms.TextInput(attrs={'class': 'form-control'}),
        #     'permanent_address': forms.TextInput(attrs={'class': 'form-control'}),
        #     'father_name': forms.TextInput(attrs={'class': 'form-control'}),
        #     'father_mobile_number': forms.TextInput(attrs={'class': 'form-control'}),
        #     'enrolled_course': forms.Select(attrs={'class': 'form-control'}),
        # }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['highest_qualification'].required = True
        self.fields['category'].required = True
        self.fields['local_address'].required = False
        # self.fields['permanent_address'].required = False
        self.fields['father_name'].required = False
        self.fields['father_mobile_number'].required = False
        self.fields['enrolled_course'].required = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].validators.append(self.name_validator)
        self.fields['email'].validators.append(self.email_validator)
        self.fields['contact'].validators.append(self.contact_validator)
        
    def save(self, commit=True):
        student = super().save(commit=False)
        user = student.user
        user = self.instance.user
        user.name = self.cleaned_data['name']
        user.email = self.cleaned_data['email']
        user.contact = self.cleaned_data['contact']
        user.highest_qualification = self.cleaned_data['highest_qualification']
        user.category = self.cleaned_data['category']
        user.local_address = self.cleaned_data['local_address']
        # user.permanent_address = self.cleaned_data['permanent_address']
        user.father_name = self.cleaned_data['father_name']
        user.father_mobile_number = self.cleaned_data['father_mobile_number']
        user.enrolled_course = self.cleaned_data['enrolled_course']

        user.save()
        student = super(self.__class__, self).save(commit=False)
        student.user = user
        if commit:
            student.save()
        return student


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['test_type', 'question_title', 'question_type', 'is_active', 'course', 'syllabus', 'frequency']
