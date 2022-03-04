from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile

def logout_users(modeladmin, request, queryset):
    queryset.update(isLogin=False)
    
logout_users.short_description = "Logout selected users"

class UserCustomize(admin.ModelAdmin):
    list_display = ('username', 'email', 'isLogin', 'loginType')
    list_filter = ('loginType',)
    actions = [logout_users]
    search_fields = ['loginType']
    save_on_top = True
    readonly_fields = ('loginType',)
    # exclude = ('description', )
    # list_display_links = ('loginType',)
    # list_select_related
    # radio_fields
    # ordering = ['date_created']
    # list_per_page = 1
    # autocomplete_fields = ['question']
    
admin.site.register(User, UserCustomize)
admin.site.register(Profile)

admin.site.site_header = "Your project name"
admin.site.site_title = "Your project name"
