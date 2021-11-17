from django.urls import path
from django.contrib import admin

from . import views

app_name = 'hcbcapacity'

urlpatterns = [
    path(r'^admin/', admin.site.urls),
    path(r'', views.index, name='index'),
    path(r'^update-api-table/', views.update_api_table, name='update-api-table' ),
    path(r'^pie-chart/', views.pie_chart, name='pie-chart'),
    path(r'^proj-wo-da/', views.proj_without_da, name='project-wo-da'),
    path('<int:prod_id>/', views.daProjects, name='da-projects'),
    path(r'^enter-info/', views.enter_info,name='enter-info'),
   
]

