# Django Imports
from django.db import models
from django.utils.translation import gettext_lazy as _

# Project Imports
from apps.accounts.models import BaseModel, User
from apps.courses.models import Courses, Syllabus


CATEGORY_CHOISES = (
    ("IT", "IT"),
    ("NON IT", "Non IT"),
)


class Student(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    highest_qualification = models.CharField(
        max_length=100)
    category = models.CharField(
        max_length=50, choices=CATEGORY_CHOISES)
    local_address = models.CharField(max_length=100, null=True, blank=True)
    permanent_address = models.CharField(max_length=100, null=True, blank=True)
    father_name = models.CharField(max_length=100, null=True, blank=True)
    father_mobile_number = models.CharField(
        max_length=100, null=True, blank=True)
    enrolled_course = models.ManyToManyField(
        Courses,
        related_name='students',
        blank=True,
    )

    def __str__(self) -> str:
        return str(self.user)


class Certificate(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    title = models.CharField(max_length=100,blank = True)
    description = models.TextField(blank =  True)
    date_issued = models.DateField(auto_now_add=True)
    certificate_file = models.ImageField(upload_to='certificates/')

    def __str__(self):
        return f"{self.student.user.username} - {self.course.course_name} Certificate"


class StudentReviews(BaseModel):
    student = models.ForeignKey(
        Student,
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    course = models.ForeignKey(
        Courses,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    rating = models.PositiveIntegerField(
        choices=(
            (1, '1'),
            (2, '2'),
            (3, '3'),
            (4, '4'),
            (5, '5'),
        )
    )
    comment = models.TextField(blank=True)
    is_approved = models.BooleanField(default= False)

    def __str__(self):
        return f"{self.course}"

STATUS_CHOISES = (
    ("None", "None"),
    ("Top", "Top"),
    ("Medium", "Medium"),
    ("Low", "Low"),
    ("Paid", "Paid"),
)

class EnquirersForms(BaseModel):
    name = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=20, unique= True)
    email = models.EmailField(unique= True)
    highest_qualification = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOISES)
    comment = models.TextField(blank =  True)
    priority = models.CharField(
        max_length=50, choices=STATUS_CHOISES)
    def __str__(self) -> str:
        return str(self.name)


class ContactForms(BaseModel):
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.CharField(max_length=200)
    message = models.CharField(max_length=100)

    def __str__(self) -> str:
        return str(self.name)


class UserCourse(models.Model):
    course_name = models.ForeignKey(
        Courses,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    student = models.ForeignKey(
        Student,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.course_name}  {self.student} "


class UserCourseModule(models.Model):

    STATUS_CHOISES = (
        ("START MODULE", "Start Module"),
        ("LOCKED", "Locked"),
        ("RUNNING", "Running"),
        ("COMPLETED", "Completed"),
    )
    course_name = models.ForeignKey(
        UserCourse,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    syllabus = models.ForeignKey(
        Syllabus,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    syllabus_status = models.CharField(
        max_length=100, choices=STATUS_CHOISES, default="LOCKED")
    
    
    def __str__(self):
        return f"{self.course_name} {self.syllabus}"

class Question(BaseModel):
    TEST_TYPE = (
        ('Practice Test','Practice Test'),
        ('Revision Test', 'Revision Test'),
        ('Monthly Test', 'Monthly Test'),
        ('FInal Test', 'FInal Test'),
    )
    QUESTION_TYPE = (
        ('Single Choise','Single Choise'),
        ('Multiple Choise', 'Multiple Choise'),
        ('Boolean Choise', 'Boolean Choise'),
        ('Text Choise', 'Text Choise'),
    )
    test_type = models.CharField(max_length=100, choices=TEST_TYPE)
    question_title = models.TextField()
    question_type = models.CharField(max_length=100, choices=QUESTION_TYPE, default="SC")
    is_active = models.BooleanField(default=True)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    syllabus = models.ForeignKey(Syllabus, on_delete=models.CASCADE)
    frequency = models.IntegerField()

    def __str__(self) -> str:
        return self.question_title
    
class Answer(BaseModel):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    choice_answer = models.TextField()
    is_correct = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.choice_answer

class RevisionTest(BaseModel):
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    syllabus = models.ForeignKey(Syllabus, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    result = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.student