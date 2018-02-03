from django.conf.urls import url
from django.urls import path,re_path
from . import views
app_name = 'WQPS'
urlpatterns = [
    path('index/', views.index, name="index"),
    path('login/', views.user_login, name="user_login"),
    path('predict/',views.predict, name="predict"),
    path('manage/',views.manage, name="manage"),
    path('logout/',views.user_logout, name="user_logout"),
    path('model/',views.model,name="model"),
    path('admin/',views.admin,name="admin"),
    re_path('',views.index),
]