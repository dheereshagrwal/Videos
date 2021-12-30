from order.models import Order
from django.db import models
from django.contrib.auth.models import User

# class UserProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     first_name = models.CharField(max_length=255, blank=True)
#     last_name = models.CharField(max_length=255, blank=True)
#     address_line_1 = models.CharField(max_length=255, blank=True)
#     address_line_2 = models.CharField(max_length=255, blank=True)
#     profile_picture = models.ImageField(
#         blank=True, upload_to='images/userprofiles')
#     country = models.CharField(max_length=255, blank=True)
#     state = models.CharField(max_length=255, blank=True)
#     city = models.CharField(max_length=255, blank=True)
#     pin = models.CharField(max_length=255, blank=True)
#     phone = models.CharField(max_length=255, blank=True)

#     def __str__(self):
#         return self.user.id

#     def full_address(self):
#         return f'{self.address_line_1} {self.address_line_2}'

#     def full_name(self):
#         return f'{self.first_name} {self.last_name}'
