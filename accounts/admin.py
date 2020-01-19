from django.contrib import admin
from .models import balance, UserProfile

# Register your models here.

admin.site.register(balance)
admin.site.register(UserProfile)