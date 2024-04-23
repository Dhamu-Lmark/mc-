from django.contrib import admin

from .models import Users, Notify, Account

# Register your models here.
admin.site.register(Users)

admin.site.register(Notify)
admin.site.register(Account)