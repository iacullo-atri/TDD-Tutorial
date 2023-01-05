from django.urls import path

from . import views

app_name='lists'
urlpatterns = [
    path('', views.index, name='index'),
    path('lists/new', views.new_list, name='new_list'),
    path('lists/the-only-list-in-the-world/', views.view_list, name='view_list'),
]
