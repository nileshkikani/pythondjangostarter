from django.db import models
from django.contrib.auth.models import AbstractUser
# from django.contrib.auth.models import User
from django.db.models import UniqueConstraint
from django.db.models.signals import post_save
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.dispatch import receiver
from django.conf import settings
# Create your models here.
class User(AbstractUser):
    isLogin = models.BooleanField(default=False)
    loginType = models.CharField(max_length=150,null=True, blank=True)
    facebookId = models.CharField(max_length=150,null=True, blank=True)
    googleId = models.CharField(max_length=150,null=True, blank=True)
    appleId = models.CharField(max_length=150,null=True, blank=True)
    forgotPasswordCode = models.CharField(max_length=150,null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.email
    
class Profile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    image = models.ImageField(null=True, blank=True, upload_to='users', height_field=None, width_field=None, max_length=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        """Meta definition for MODELNAME."""
        db_table = "profiles"
        # verbose_name = 'MODELNAME'
        # verbose_name_plural = 'MODELNAMEs'

class User_Additional_Field(models.Model):
    userName = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# class Sauce(models.Model):
#     name = models.CharField(max_length=100)

#     def __str__(self):
#         return self.name

# class Sandwich(models.Model):
#     name = models.CharField(max_length=100)
#     sauces = models.ManyToManyField(Sauce)

#     def __str__(self):
#         return self.name


# Sandwich.objects.filter(sauces__name="Barbeque sauce")

# @receiver(post_save, sender=User)
# def send_welcome_email(sender, instance, created, **kwargs):
#     print("----------instance",instance)
#     if created:
#         # Profile.objects.create(user=instance)
#         subject = 'Welcome to our Django project!'
#         html_message = render_to_string('accounts/email_template.html', {'label': "Hello,", 'value': "Good to know you registered with us!"})
#         plain_message = strip_tags(html_message)
#         from_email = 'adityapandya948@gmail.com'
#         to = instance.email
#         send_mail(
#             subject, plain_message, from_email, [to], html_message=html_message
#         )
