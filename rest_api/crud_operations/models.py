from django.db import models

# Create your models here.

class Task(models.Model):
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class SpaceList(models.Model):
    spaceName = models.CharField(max_length=150,null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.spaceName

class SpaceFeature(models.Model):
    feature = models.CharField(max_length=150,null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.feature

class SpaceFeatureList(models.Model):
    # spaceNames = models.ForeignKey(SpaceList, related_name="x", on_delete=models.CASCADE, null=True, db_column='spaceListId') 
    # spaceFeatures = models.ManyToManyField(SpaceFeature, related_name="y", db_column='spaceFeatureId')
    spaceNames = models.ForeignKey(SpaceList, related_name="x", on_delete=models.CASCADE, null=True) 
    spaceFeatures = models.ManyToManyField(SpaceFeature, related_name="y")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        """Meta definition for MODELNAME."""
        db_table = " spaceFeatureLists"
        # verbose_name = 'MODELNAME'
        # verbose_name_plural = 'MODELNAMEs'

    def __str__(self):
        return self.spaceNames.spaceName

    def get_space_features(self):
        return self.spaceFeatures.all().values()