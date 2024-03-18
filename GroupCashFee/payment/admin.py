from django.contrib import admin
from payment.models import Reason, Collect, Attendee, Account, Action, Payment




admin.site.register(Reason)
admin.site.register(Collect)
admin.site.register(Attendee)
admin.site.register(Account)
admin.site.register(Action)
admin.site.register(Payment)
