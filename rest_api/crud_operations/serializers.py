from rest_framework import serializers
from . import models

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Task
        fields = '__all__'

class ManyToManyDemoSerializer(serializers.Serializer):
    featureName = serializers.CharField(required=True)
    featureName1 = serializers.CharField(required=True)

class AddFeaturesToSpaceSerializer(serializers.Serializer):
    spaceName = serializers.CharField(required=True)    
    featureList = serializers.ListField(child=serializers.CharField())