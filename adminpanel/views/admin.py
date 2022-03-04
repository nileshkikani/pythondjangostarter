from django.http import QueryDict
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from rest_framework import status
from rest_framework.response import Response

from ..models import Admin
from ..serializers import AdminSerializer


@require_http_methods(["GET"])
def index(request):
    return render(request, 'admin/index.html')


@require_http_methods(["GET"])
def create(request):
    return render(request, 'admin/create.html')


@require_http_methods(['POST'])
def store(request):
    # inputs = QueryDict.dict(request.POST) # convert into object
    inputs = request.POST
    adminRequest = Admin(
        name=inputs["name"], email=inputs["email"], password=inputs["password"])
    adminRequest.password = adminRequest.makePassword()
    adminRequest.save()
    messages.success(request, 'Admin create successfully')
    return redirect('/admin/admin-user')


@require_http_methods(['GET'])
def edit(request, id):
    admin = Admin.objects.get(id=id)
    return render(request, 'admin/edit.html', {'result': admin})


@require_http_methods(['POST'])
def update(request, id):
    inputs = request.POST
    admin = Admin.objects.get(id=id)
    admin.name = inputs["name"]
    admin.email = inputs["email"]
    admin.save()

    messages.success(request, 'Admin update successfully')
    return redirect('/admin/admin-user')


@require_http_methods(["GET"])
def datatable(request):
    result = Admin.datatableQuery(request.GET)
    serializer_data = AdminSerializer(result['data'], many=True)
    result['data'] = serializer_data.data

    return JsonResponse(result)


def destroy(request, id):
    if request.method != "DELETE":
        return JsonResponse({"message": 'Method not allowed'}, 400)

    Admin.objects.get(id=id).delete()
    response = {"message": "Admin delete successfully"}
    return JsonResponse(response)


@require_http_methods(["GET"])
def show(request, id):
    admin = Admin.objects.get(id=id)
    return render(request, 'admin/view.html', {'result': admin})
