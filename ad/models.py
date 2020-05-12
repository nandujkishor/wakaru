from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Token(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    time = models.DateTimeField(default=timezone.now)