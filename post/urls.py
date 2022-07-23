from django.urls import path
from . import views

urlpatterns=[
    path('list/', views.getList),
    path('read/<int:num>/', views.read),
    path('write/', views.write),
    path('update/', views.update),
    path('remove/', views.delete),
    path('addcomment/', views.addComment),
]