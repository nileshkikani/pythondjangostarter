from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.apiOverview, name='api-overview'),
    path('task-create/', views.taskCreate, name='task-create'),
    path('task-list/', views.taskList, name='task-list'),
    path('task-detail/<int:pk>', views.taskDetail, name='task-detail'),
    path('task-update/<int:pk>', views.taskUpdate, name='task-update'),
    path('task-delete/<int:pk>', views.taskDelete, name='task-delete'),
    re_path(r'^many-to-many/$', views.ManyToManyDemo,),
    path('add-features-to-space/', views.AddFeaturesToSpace, name="add-features-to-space"),
]