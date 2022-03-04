from rest_framework import serializers
from rest_framework.validators import UniqueValidator
# from django.contrib.auth.models import User
from .models import User, Profile
import time
# from .models import User_Additional_Field
# from .models import CustomUser

class UserSerializer(serializers.Serializer):
    
    # def validate(self, data):
    #     """
    #     Check if email exists.
    #     """
                
    #     if User.objects.get(email=data['email']):
    #         raise serializers.ValidationError("Email already exist!")            
    #     return data        
    
    # class Meta:
    #     model = User
    #     fields = ('email','password')
    
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def create(self, validated_data):
        splitValues = validated_data['email'].split('@')
        user = User(
            username= splitValues[0] + "_" + str(round(time.time() * 1000)),
            email=validated_data['email']
        )
        # userExtraFields = User_Additional_Field(userName=user)
        user.set_password(validated_data['password'])
        print("------called second")
        user.save()
        # userExtraFields.save()   
        # print("----------user",type(user))
        return user

    # Override serialization behavior if want to remove fields from serialize.data
    def to_representation(self, obj):
        # get the original representation
        ret = super(UserSerializer, self).to_representation(obj)

        # remove 'url' field if mobile request
        
        ret.pop('password')

        # here write the logic to check whether `elements` field is to be removed 
        # pop 'elements' from 'ret' if condition is True

        # return the modified representation
        return ret 
    
class UserLoginSerializer(serializers.Serializer):
    
    # allow_blank=True will allow you to pass "" (i.e blank) from postman but then you have to handle validation by yourself
    email = serializers.EmailField(required=False)
    password = serializers.CharField(required=False)
    isLogin = serializers.BooleanField(required=False)
    loginType = serializers.CharField(required=True)
    socialId = serializers.CharField(required=False)    
    
    # def get_validation_exclusions(self):
    #     exclusions = super(UserLoginSerializer, self).get_validation_exclusions()
    #     return exclusions + ['password']
    
    
class UserForgotPasswordSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    

class UserListSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = ('id','email')

class UserUpdateSerializer(serializers.Serializer):
    facebookId = serializers.CharField(required=False)
    appleId = serializers.CharField(required=False)
    googleId = serializers.CharField(required=False)
    
    # class Meta:
    #     model = User
    #     fields = ('facebookId','appleId','googleId')
        
class FileListSerializer(serializers.Serializer) :
    email = serializers.CharField(required=True)
    image = serializers.ListField(
                       child=serializers.FileField( max_length=100000,
                                         allow_empty_file=False,
                                         use_url=False ))