from django.urls import path

from . import views

app_name = 'courses'
urlpatterns = [
    path('<code>/', views.course, name='course'),
    path('<code>/<int:lecture>/add/page/', views.addpage, name='addpage'),
    path('<code>/<int:lecture>/<hash>/<title>/<int:id>/', views.viewpage, name='viewpage'),
    path('<code>/<int:lecture>/<content>/', views.editlecture, name="editlecture"),
    path('<code>/lecture/new/', views.newlecture, name="newlecture")
]