# from .models import User
# from .jwtToken import EncodeData, DecodeData
# from rest_framework import authentication
# from rest_framework.response import Response
# from rest_framework import status

# class CustomAuthentication(authentication.BaseAuthentication):
    
#     # def __init__(self, *args, **kwargs):
#     #     print("data",args)
#     #     self.email = args['email']
#     #     self.password = args['password']
    
#     def authenticate(self, request):
#         print(request.data)
#         email = request.data['email']
#         password = request.data['password']
#         if not email or not password:
#             Response(data={"data": "", "message": "Email and password is required!", "status": status.HTTP_400_BAD_REQUEST})

#         try:
#             user = User.objects.get(email=email) # get the user
#         except User.DoesNotExist:
#             Response(data={"data": "", "message": "Signup first!", "status": status.HTTP_400_BAD_REQUEST})

#         encoded_jwt = EncodeData({"id": user.id})
#         return user
#         # return "Hi"