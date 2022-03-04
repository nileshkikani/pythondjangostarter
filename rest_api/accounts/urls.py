from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView
from django.conf.urls.static import static
from django.conf import settings
from graphene_file_upload.django import FileUploadGraphQLView

urlpatterns = [
    path('register/', views.UserRegister, name="register"),
    path('login/', views.UserLogin, name="login"),
    path('logout/', views.UserLogout, name="logout"),
    path('forgot-password/', views.UserForgotPassword, name="forgot-password"),
    path('set-new-password/', views.UserSetNewPassword, name="set-new-password"),
    path('password-set-success/', views.UserSetPasswordSuccess, name="password-set-success"),
    path('test/', views.test, name="test"),
    path('user-list/', views.UserList, name="user-list"),
    # re_path(r'^many-to-many/(?P<featureName>.+)/$', views.ManyToManyDemo,),    
    path("graphql", csrf_exempt(GraphQLView.as_view(graphiql=True))),
    path("file-upload/graphql", csrf_exempt(FileUploadGraphQLView.as_view(graphiql=True))),
    path('update-user/<str:pk>/', views.UserUpdate, name="update-user"),
    path('upload-multiple-images/', views.UploadImages, name="upload-multiple-images"),
]