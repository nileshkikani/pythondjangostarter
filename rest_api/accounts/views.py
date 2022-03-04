from django.shortcuts import render, redirect
from django.db import IntegrityError
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import *
# from django.contrib.auth.models import User
from .models import User, Profile
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from django.core import serializers
import json
import time
from django.forms.models import model_to_dict
from .models import User_Additional_Field
from django.contrib.auth.decorators import login_required
from .jwtToken import EncodeData, DecodeData
from .decorators import isUserAuthenticated
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import os
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from .forms import UserSetPassword
from django.contrib import messages
from rest_framework.pagination import CursorPagination, PageNumberPagination
from rest_framework import authentication
from rest_framework import exceptions
from django.db import connection
cursor = connection.cursor()
from django.conf import settings
# from .customAuth import EmailBackend
# from .authentication import CustomAuthentication
# from rest_framework.authentication import BasicAuthentication
# from django.views.defaults import bad_request
# import jwt
# Create your views here.


# class CustomAuthentication(authentication.BaseAuthentication):
#     def authenticate(self, request, validated_data):
#         print("request, validated_data", validated_data)
#         email = validated_data['email']
#         password = validated_data['password']
#         if not email or not password: # no username passed in request headers
#             Response(data={"data": "", "message": "Email and password is required!", "status": status.HTTP_400_BAD_REQUEST})

#         try:
#             user = User.objects.get(email=email) # get the user
#         except User.DoesNotExist:
#             Response(data={"data": "", "message": "Signup first!", "status": status.HTTP_400_BAD_REQUEST})

#         encoded_jwt = EncodeData({"id": user.id})
#         return Response(data={"data": {"users" : model_to_dict(user,exclude="password")}, "message": "Logged in!", "token": encoded_jwt, "status": status.HTTP_200_OK})
#         # return Response(data={"data": {"users" : ""}, "message": "Logged in!", "token": "", "status": status.HTTP_200_OK})

def UserSetNewPassword(request):
    
    if request.method == 'POST':        
        form = UserSetPassword(request.POST)
        if form.is_valid():
            print("-------in form valid",form.cleaned_data)
            forgotPasswordCode = form.cleaned_data.get('code')
            try:
                userExtraDetails = User.objects.get(forgotPasswordCode=forgotPasswordCode)
            except ObjectDoesNotExist as e:
                return HttpResponse('<h4>Code you entered is incorrect!</h4>')
            # user = User.objects.get(username=userExtraDetails.userName)
            userExtraDetails.set_password(form.cleaned_data.get('new_password'))
            userExtraDetails.save()
            return redirect('password-set-success')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = UserSetPassword()

    return render(request, 'accounts/forgot-password.html', {'form': form})

   
def UserSetPasswordSuccess(request):
    return render(request, "accounts/password-set-success.html")

@api_view(['POST'])
def UserRegister(request):    
        
    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():        
        try :
            # if 'email' not in serializer.validated_data or not serializer.validated_data['email']:
            # return Response(data={"data": "", "message": "Email is required!", "status": status.HTTP_400_BAD_REQUEST})
            User.objects.get(email=serializer.validated_data['email'])
            return Response(data={"data": "", "message": "Email exist!", "status": status.HTTP_400_BAD_REQUEST})
        except ObjectDoesNotExist:
            print("------called first")           
            serializer.save()            
            print(serializer.data)
            return Response(data={"data": serializer.data, "message": "User created successfully!",  "status": status.HTTP_200_OK})
    else:        
        print("------called first in else")
        print("----------serializer.errors",list(serializer.errors.items())[0][0])
        return Response(data={"data": "", "message": serializer.errors, "status": status.HTTP_400_BAD_REQUEST})            
    
        
@api_view(['POST'])
def UserLogin(request):
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        print("------serializer.validated_data",serializer.validated_data)
        # u = EmailBackend()
        # user = u.authenticate(request,serializer.validated_data['email'],serializer.validated_data['password'])
        # encoded_jwt = EncodeData({"id": user.id})
        # return Response(data={"data": {"users" : model_to_dict(user,exclude="password")}, "message": "Logged in!", "token": encoded_jwt, "status": status.HTTP_200_OK})
        try:        
            if serializer.validated_data['loginType'] == 'email' and 'email' in serializer.validated_data and 'password' in serializer.validated_data:
                user = User.objects.get(email=serializer.validated_data['email'])
                print("-------user", user.email)
                # print("-------------",User.objects.get(pk=1).User_Additional_Field_set.all())        
                
                if user.isLogin == True:
                    return Response(data={"data": "", "message": "User already logged-in!", "status": status.HTTP_400_BAD_REQUEST})
                
                if user.check_password(serializer.validated_data['password']):                    
                    encoded_jwt = EncodeData({"id": user.id})
                    # We get tuple in response so did userExtraRecord, created to get model instance in userExtraRecord
                    userExtraRecord, created = User.objects.defer('password').update_or_create(email=user.email, defaults={'isLogin': True, 'loginType': serializer.validated_data['loginType']})                               
                    # ------ For single object
                    # model_to_dict(user)
                    # ------ For multiple objects
                    # User.objects.values()
                    return Response(data={"data": {"users" : model_to_dict(userExtraRecord,exclude="password")}, "message": "Logged in!", "token": encoded_jwt, "status": status.HTTP_200_OK})
                
                else:
                    return Response(data={"data": "", "message": "Either email or password is incorrect!", "status": status.HTTP_400_BAD_REQUEST})
            
            elif serializer.validated_data['loginType'] == 'facebook' and 'socialId' in serializer.validated_data:
                
                try:                    
                    getUserRecord = User.objects.get(loginType=serializer.validated_data['loginType'],facebookId=serializer.validated_data['socialId'])                    
                
                    if getUserRecord.isLogin == True:
                        return Response(data={"data": "", "message": "User already logged-in!", "status": status.HTTP_400_BAD_REQUEST})
                    
                    else:
                        userExtraRecord, created = User.objects.update_or_create(facebookId=getUserRecord.facebookId, defaults={'isLogin': True})                        
                        # user = User.objects.get(username=userExtraRecord.userName)
                        encoded_jwt = EncodeData({"id": userExtraRecord.id})
                        return Response(data={"data": {"users" : model_to_dict(userExtraRecord,exclude="password")}, "message": "Logged in!", "token": encoded_jwt, "status": status.HTTP_200_OK})                                   
                
                except ObjectDoesNotExist:
                    
                    createUserRecord = User.objects.create(username=serializer.validated_data['loginType'] + "_"+ str(round(time.time() * 1000)),loginType=serializer.validated_data['loginType'],facebookId=serializer.validated_data['socialId'],isLogin=True)
                    createUserRecord.set_unusable_password()
                    createUserRecord.save()
                    encoded_jwt = EncodeData({"id": createUserRecord.id})
                    # userExtraRecord = User_Additional_Field.objects.create(userName=createUserRecord,loginType=serializer.validated_data['loginType'],facebookId=serializer.validated_data['socialId'],isLogin=True)    
                    return Response(data={"data": {"users" : model_to_dict(createUserRecord,exclude="password")}, "message": "Logged in!", "token": encoded_jwt, "status": status.HTTP_200_OK})
            else:
                return Response(data={"data": "", "message": "Input parameter combination is incorrect!", "status": status.HTTP_400_BAD_REQUEST})
        except ObjectDoesNotExist:
            return Response(data={"data": "", "message": "Please signup first!", "status": status.HTTP_400_BAD_REQUEST})        
    else:
        print("------called first in else login")        
        return Response(data={"data": "", "message": serializer.errors})
# list(serializer.errors.values())[0][0]


@api_view(['POST'])
@isUserAuthenticated
def UserLogout(request, userId):    
    if type(userId) is dict:
        userName = User.objects.get(pk=userId['id'])
        print("------userName.username",userName)
        # User.objects.update_or_create(username=userName.id, defaults={'isLogin': False})    
        User.objects.update_or_create(email=userName.email, defaults={'isLogin': False})  
        return Response(data={"data": "", "message": "Logged-out successfully"})
    else:
        return Response(data={"data": "", "message": userId})


@api_view(['POST'])
def UserForgotPassword(request):    
    serializer = UserForgotPasswordSerializer(data=request.data)
    if serializer.is_valid():        
        try :
            user = User.objects.get(email=serializer.validated_data['email'])
            # user.set_password(serializer.validated_data['password'])
            randomCode = "pass_" + str(round(time.time() * 1000))
            User.objects.update_or_create(username=user.username, defaults={'forgotPasswordCode': randomCode})
            # print("-----link",request.META['HTTP_HOST'] + "/accounts/set-new-password/")
            # print("c",c)
            subject = 'Forgot password request!'
            html_message = render_to_string('accounts/email_forgot_password.html', {'link': request.build_absolute_uri('/accounts/set-new-password/'), 'code': randomCode})
            plain_message = strip_tags(html_message)
            from_email = 'adityapandya948@gmail.com'
            to = serializer.validated_data['email']
            send_mail(
               subject, plain_message, from_email, [to], html_message=html_message
            )
            return Response(data={"data": "", "message": "Check your email for new password!", "status": status.HTTP_200_OK})
        except ObjectDoesNotExist:
            return Response(data={"data": "", "message": "Email doesn't exist!", "status": status.HTTP_400_BAD_REQUEST})
    else:
        print("------called first in else")
        print("----------serializer.errors",serializer.errors)
        return Response(data={"data": "", "message": serializer.errors})            
        


@api_view(['POST'])
def test(request):
    print(request.data)
    
    
class CustomPagination(PageNumberPagination):    
    def get_paginated_response(self, data):
        
        return Response(data={"data":
            # 'links': {
            #     'next': self.get_next_link(),
            #     'previous': self.get_previous_link()
            # },
            {
            'count': self.page.paginator.count,
            'page_size': self.page_size,
            'data': data
            }
        })
        
class ListAsQuerySet(list):

    def __init__(self, *args, model, **kwargs):
        self.model = model
        super().__init__(*args, **kwargs)

    def filter(self, *args, **kwargs):
        return self  # filter ignoring, but you can impl custom filter

    def order_by(self, *args, **kwargs):
        return self

@api_view(['GET'])
def UserList(request):
    users = User.objects.raw('SELECT id,email FROM accounts_user')
    # c =  cursor.execute('''SELECT id,email FROM accounts_user''')
    # print(c)
    # row = cursor.fetchall()
    # print(row)
    arr = []
    for u in users:
        arr.append({'id': u.id, 'email': u.email})
    print(arr)
    qs = ListAsQuerySet(arr, model=User)
    users = User.objects.all()
    paginator = CustomPagination()
    paginator.page_size = 2
    # person_objects = Person.objects.all()
    result_page = paginator.paginate_queryset(qs, request)
    print("result_page",result_page)
    # serializer = UserListSerializer(result_page, many=True)
    return paginator.get_paginated_response(result_page)    
    # return Response(data={"data": serializer.data,"message": "List fetched successfully!"})
    

@api_view(['POST'])
def UserUpdate(request, pk):    
    try:
        user = User.objects.get(id=pk)
    except ObjectDoesNotExist:
        return Response(data={"data": "", "message": "That id doesn't exist!", "status": status.HTTP_400_BAD_REQUEST})
    
    serializer = UserUpdateSerializer(data=request.data)
    # serializer = UserUpdateSerializer(instance=user, data=request.data)
    
    if serializer.is_valid():        
        try :
            # if 'email' not in serializer.validated_data or not serializer.validated_data['email']:
            # return Response(data={"data": "", "message": "Email is required!", "status": status.HTTP_400_BAD_REQUEST})
            # serializer.save()
            User.objects.update_or_create(email=user.email, defaults=serializer.validated_data) 
            return Response(data={"data": "", "message": "success!", "status": status.HTTP_200_OK})
        except ObjectDoesNotExist:
            print("------called first")           
            serializer.save()            
            print(serializer.data)
            return Response(data={"data": serializer.data, "message": "User created successfully!",  "status": status.HTTP_200_OK})
    else:        
        print("------called first in else")
        print("----------serializer.errors",list(serializer.errors.items())[0][0])
        return Response(data={"data": "", "message": serializer.errors, "status": status.HTTP_400_BAD_REQUEST})
    
@api_view(['POST'])
def UploadImages(request):    
    
    print("---request",request, request.data)
    # return Response(data={"data": "", "message": "Files uploaded successfully!",  "status": status.HTTP_200_OK})
    serializer = FileListSerializer(data=request.data)
    # # serializer = UserUpdateSerializer(instance=user, data=request.data)
    
    if serializer.is_valid():        
        try :
            # if 'email' not in serializer.validated_data or not serializer.validated_data['email']:
            # return Response(data={"data": "", "message": "Email is required!", "status": status.HTTP_400_BAD_REQUEST})
            # serializer.save()
            print("----serializer.validated_data",serializer.validated_data)
            user = User.objects.get(email=serializer.validated_data['email'])
            for img in serializer.validated_data['image']:
                photo=Profile.objects.create(image=img,user=user)
                print(settings.MEDIA_PATH + "/" + str(photo.image))
            # profile =Profile.objects.create(user=user)
            # profile.image.set(serializer.validated_data['image'])
            return Response(data={"data": "", "message": "success!", "status": status.HTTP_200_OK})
        except ObjectDoesNotExist:
            print("------called first")           
            serializer.save()            
            print(serializer.data)
            return Response(data={"data": serializer.data, "message": "User created successfully!",  "status": status.HTTP_200_OK})
    else:        
        print("------called first in else")
        print("----------serializer.errors",list(serializer.errors.items())[0][0])
        return Response(data={"data": "", "message": serializer.errors, "status": status.HTTP_400_BAD_REQUEST})