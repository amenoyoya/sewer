from django.urls import path 
from . import views 

app_name='pyapp' 

urlpatterns = [
    path('', views.login, name='login'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('mypage/', views.mypage, name='mypage'),
    path('request/', views.request_constract, name='request'),
    path('preview/', views.preview_constract, name='preview'),
]