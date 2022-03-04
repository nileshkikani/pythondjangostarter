
from rest_framework.response import Response
from .jwtToken import EncodeData, DecodeData
from django.shortcuts import redirect

def isUserAuthenticated(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.headers.get('Authorization') is None:
            print("---------in",request)
            return Response(data={"data": "", "message": "Authorization header not found"})
        else:
            userToken = request.headers.get('Authorization').split(" ")[1]
            userId = DecodeData(userToken)
            return view_func(request, userId, **kwargs)
    return wrapper_func

def isUserAuthenticatedGraphQL(view_func):
    def wrapper_func(root, info, userId=None):
        print("in")
        print(info.context.META.get('HTTP_AUTHORIZATION'))
        if info.context.META.get('HTTP_AUTHORIZATION') is None:
            raise Exception("Authorization header not found!")
        else:
            userToken = info.context.META.get('HTTP_AUTHORIZATION').split(" ")[1]
            userId = DecodeData(userToken)
        return view_func(root, info, userId)
    return wrapper_func