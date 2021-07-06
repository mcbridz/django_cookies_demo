from django.db import models
from django.contrib.auth.models import User


# class UserProfile(models.Model):
#     login_name = models.OneToOneField(
#         User, on_delete=models.CASCADE, related_name='profile_ref')

#     def __str__(self):
#         return self.login_name.last_name + ', ' + self.login_name.first_name
