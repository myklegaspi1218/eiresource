from django.urls import path
from django.contrib import admin

from . import views

app_name = 'hcbcapacity'

urlpatterns = [
   
    path('index/', views.index, name='index'),
    path('update-api-table/', views.update_api_table, name='update-api-table' ),
    path('pie-chart/', views.pie_chart, name='pie-chart'),
    path('proj-wo-da/', views.proj_without_da, name='project-wo-da'),
    path('<int:prod_id>/', views.daProjects, name='da-projects'),
    path('enter-info/', views.enter_info,name='enter-info'),
   
]

