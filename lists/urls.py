from django.urls import path

from . import views

app_name='lists'
urlpatterns = [
    path('', views.index, name='index'),
    path('lists/new', views.new_list, name='new_list'),
    path('lists/<int:list_id>/', views.view_list, name='view_list'),
    path('lists/<int:list_id>/new', views.add_item, name='add_item'),
]
