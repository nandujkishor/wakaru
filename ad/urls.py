from django.urls import path

from . import views

app_name = 'ad'
urlpatterns = [
    path('login/', views.sendtomicrosoft, name="send"),
    path('response/', views.returnfrommicrosoft, name="return"),
]