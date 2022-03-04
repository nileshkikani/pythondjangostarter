from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import *
from .models import SpaceList, SpaceFeature, SpaceFeatureList
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.

@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'List': '/task-list/',
        'Details View': '/task-detail/<int:pk>',
        'Create': '/task-create/',
        'Update': '/task-update/<int:pk>',
        'Delete': '/task-delete/<int:pk>'
    }
    return JsonResponse(api_urls)

@api_view(['POST'])
def taskCreate(request):    
    serializer = TaskSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        print(serializer.data)
    
    return Response(serializer.data)

@api_view(['GET'])
def taskList(request):
    tasks = Task.objects.all()
    serializer = TaskSerializer(tasks, many=True)
    return JsonResponse(data={"data": serializer.data[0]})

@api_view(['GET'])
def taskDetail(request, pk):
    try:
        task = Task.objects.get(id=pk)
    except:
        return Response("That id doesn't exist")    
    serializer = TaskSerializer(task, many=False)
    print(type(serializer.data))
    return JsonResponse(data={"data": serializer.data, "message": "Details fetched successfully!"})

@api_view(['POST'])
def taskUpdate(request, pk):
    task = Task.objects.get(id=pk)
    serializer = TaskSerializer(instance=task, data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)

@api_view(['DELETE'])
def taskDelete(request, pk):
    task = Task.objects.get(id=pk)
    task.delete()

    return Response("Item successfully deleted")

@api_view(['GET'])
def ManyToManyDemo(request):
    
    # --------- create first a foreign key object and then set data to many-to-many field
    
    # spaceList = SpaceList.objects.get(spaceName="Bhaktinagar")
    # spaceFeatures = SpaceFeature.objects.filter(feature__in=["feature1","feature2"])
    # sName = SpaceFeatureList.objects.create(spaceNames=spaceList)
    # sName.spaceFeatures.set(spaceFeatures)    
   
    # ------------------------ #
    
    # --------- update data to many-to-many field, use set() here also
    
    # spaceList = SpaceList.objects.get(spaceName="Bhaktinagar")
    # sList = SpaceFeatureList.objects.get(spaceNames=spaceList.id)
    # spaceFeatures = SpaceFeature.objects.filter(feature="feature3")
    # sList.spaceFeatures.set(spaceFeatures) # Here feature1, feature2 will be replaced by feature3
        
    # ------------------------ #
    
    # --------- delete an object that has foreign key 
    
    # SpaceFeatureList.objects.filter(spaceNames=3).delete()
    
    # ------------------------ #
    
    # --------- select_related is a performance booster for foreign key relationships 
    
    # In shell logs, check this
        # space = SpaceList.objects.get(id=1)
        # SpaceFeatureList.objects.get(spaceNames=space.id) # This will fire 2 queries
    # and this
        # SpaceFeatureList.objects.select_related("spaceNames").get(spaceNames=space.id) # This will fire 1 query
    
    # ------------------------ #
    
    # --------- prefetch_related is a performance booster for many-to-many relationships 
    
    # In shell logs, check this
        # space = SpaceList.objects.get(id=1)
        # The below two commands will result into 2 queries
        # s = SpaceFeatureList.objects.get(spaceNames=space.id)
        # s.spaceFeatures.all()
    # and below 2 commands will fire 1 query
        # SpaceFeatureList.objects.prefetch_related("spaceFeatures").get(spaceNames=space.id)
        # s.spaceFeatures.all()
    # ------------------------ #
    
    # print("request.data",request.GET.get('featureName', ''))
    print("request",request.GET)
    serializer = ManyToManyDemoSerializer(data=request.GET)
    if serializer.is_valid():
        # print("--------",serializer.validated_data['featureName'])
        arr = []
        # result = SpaceFeatureList.objects.filter(spaceFeatures__feature=serializer.validated_data['featureName'])
        result = SpaceFeatureList.objects.filter(spaceFeatures__feature__in=[serializer.validated_data['featureName'],serializer.validated_data['featureName1']]).distinct()
        print("---------result", result)
        for r in result:
            # print(r.spaceFeatures.all().values())
            arr.append({"space": r.spaceNames.spaceName})
        return Response(data={"data": arr, "message": "success"}) 
    else:
        print("------called first in else login")
        return Response(data={"data": "", "message": serializer.errors})  


@api_view(['POST'])
def AddFeaturesToSpace(request):
    print("request",request.data)
    # return Response(data={"data": "", "message": ""})  
    serializer = AddFeaturesToSpaceSerializer(data=request.data)
    if serializer.is_valid():
        try:
            spaceListRecord = SpaceList.objects.get(spaceName=serializer.validated_data['spaceName'])
            SpaceFeatureListRecord = SpaceFeatureList.objects.get(spaceNames=spaceListRecord.id)
            spaceFeatures = SpaceFeature.objects.filter(feature__in=serializer.validated_data['featureList'])
            SpaceFeatureListRecord.spaceFeatures.set(spaceFeatures)
        except ObjectDoesNotExist:
            spaceListRecord = SpaceList.objects.get(spaceName=serializer.validated_data['spaceName'])
            SpaceFeatureListRecord = SpaceFeatureList.objects.create(spaceNames=spaceListRecord)
            spaceFeatures = SpaceFeature.objects.filter(feature__in=serializer.validated_data['featureList'])
            print("---spaceFeatures",spaceFeatures)
            SpaceFeatureListRecord.spaceFeatures.set(spaceFeatures)
        
        # print("--------",serializer.validated_data['featureName'])
        # arr = []
        # # result = SpaceFeatureList.objects.filter(spaceFeatures__feature=serializer.validated_data['featureName'])
        # result = SpaceFeatureList.objects.filter(spaceFeatures__feature__in=[serializer.validated_data['featureName'],serializer.validated_data['featureName1']]).distinct()
        # for r in result:
        #     print(r.spaceNames.all()[0])
        #     arr.append(r.spaceNames.all().values()[0])
        return Response(data={"data": "", "message": "success"}) 
    else:
        print("------called first in else login")
        return Response(data={"data": "", "message": serializer.errors}) 