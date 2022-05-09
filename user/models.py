from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

class Profile(User):
    address = models.TextField(null= True, blank= True)
    mobile_phone_number = models.CharField(null=True, max_length=10, validators=[RegexValidator(r'^9\d{9}$')])
    join_date = models.DateField(auto_now_add=True)