from django.urls import path
from .views import admin
from .views import auth
from .decorators import login_is_required

urlpatterns = [
    path('login',auth.login,name="login"),
    path('login-check',auth.loginCheck,name="login_check"),
    path('logout',auth.logout),

    path('admin-user', login_is_required(admin.index), name="admin_user"),
    path('admin-user/create', login_is_required(admin.create), name="admin_user_create"),
    path('admin-user/store',login_is_required(admin.store),name="admin_user_store"),
    path('admin-user/<int:id>/edit',login_is_required(admin.edit),name="admin_user_edit"),
    path('admin-user/<int:id>',login_is_required(admin.show),name="admin_user_view"),
    path('admin-user/update/<int:id>',login_is_required(admin.update),name="admin_user_update"),
    path('admin-user/datatable',login_is_required(admin.datatable),name='admin_user_datatable'),
    path('admin-user/delete/<int:id>',login_is_required(admin.destroy),name="admin_user_destroy")
]
