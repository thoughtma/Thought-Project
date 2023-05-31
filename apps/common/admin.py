# Django Import
from django.contrib import admin
from .models import OurOffices, NewsletterSubscriber

# Project Import
from .models import Paymentlog


class PaymentlogAdmin(admin.ModelAdmin):
    list_display = [
        'order_type',
        'order_id',
        'transaction_id',
        'paymentdate',
        'price',
        # 'studentid',
    ]


admin.site.register(Paymentlog, PaymentlogAdmin)


class OurOfficesAdmin(admin.ModelAdmin):
    list_display = [
        'office_name',
        'address',
        'contact',
        'email'
    ]


admin.site.register(OurOffices, OurOfficesAdmin)


admin.site.register(NewsletterSubscriber)