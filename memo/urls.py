from django.urls import path
from . import views

urlpatterns=[
    path('list/', views.getList),
    path('write/', views.write),
    path('update/', views.update),
    path('remove/', views.delete),
]