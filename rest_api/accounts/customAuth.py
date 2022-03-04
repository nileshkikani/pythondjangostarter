# from django.contrib.auth import get_user_model
# from django.contrib.auth.backends import ModelBackend

# class EmailBackend(ModelBackend):
#     def authenticate(self, request, username, password, **kwargs):
#         UserModel = get_user_model()
#         print("------ in EmailBackend")
#         try:
#             user = UserModel.objects.get(email=username)
#             print("------user",user)  
#         except UserModel.DoesNotExist:
#             return None
#         else:
#             if user.check_password(password):
#                 return user
#         return None