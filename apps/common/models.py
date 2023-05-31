# Django Imports 
from django.db import models
from django.utils.translation import gettext_lazy as _

# Project Imports
from apps.accounts.models import BaseModel
# from apps.student.models import Student


# class AddOns(BaseModel):
#     trainer_name = models.ForeignKey(
#         'Trainer',
#         null=True,
#         blank=True,
#         on_delete=models.SET_NULL,
#     )
#     contact = models.IntegerField()
#     email = models.EmailField()

#     def __str__(self) -> str:
#         return str(self.trainer_name)


class OurOffices(BaseModel):
    office_name = models.CharField(max_length=200, null=True, blank=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    contact = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    

class Paymentlog(BaseModel):
    ordertypes=[('buynow','Regular'),('subscription','Subscription')]
    order_type=models.CharField(choices=ordertypes,max_length=200)
    order_id=models.CharField(max_length=200)
    transaction_id=models.CharField(max_length=200)
    paymentdate=models.DateTimeField(auto_now_add=True)
    price=models.DecimalField(max_digits=6,decimal_places=2,default='00.00')
    # studentid=models.ForeignKey(Student,on_delete=models.DO_NOTHING,default="")


class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    is_subscribed = models.BooleanField(default=True)

    def __str__(self):
        return self.email
    
    