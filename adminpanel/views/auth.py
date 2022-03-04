from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.core import serializers

from ..models import Admin


@require_http_methods(["GET"])
def login(request):
    return render(request, 'auth/login.html')


@require_http_methods(["POST"])
def loginCheck(request):
    inputs = request.POST
    adminResult = ''
    try:
        adminResult = Admin.objects.get(email=inputs['email'])
        success = adminResult.checkPassword(inputs['password'])

        if success:
            # serializers.serialize("json", [adminResult])
            # request.session['user']=serializers.serialize("json", [adminResult])
            request.session['user'] = {"name": getattr(adminResult, "name"), "id": getattr(adminResult, "id")}
            return redirect('admin_user')
        else:
            messages.error(request, 'Credentials do not match our records.')
            return redirect('login')

    except ObjectDoesNotExist:
        pass
        messages.error(request, 'Credentials do not match our records.')
        return redirect('login')


@require_http_methods(["POST"])
def logout(request):
    del request.session["user"]
    return redirect('login')
