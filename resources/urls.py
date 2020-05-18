from django.urls import path

from . import views

app_name = 'resources'
urlpatterns = [
    path('<code>/<lecture>/', views.add, name='addresource'),
    path('video/', views.video, name="video")
]