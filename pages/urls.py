from django.urls import path

from . import views

app_name = 'pages'
urlpatterns = [
    path('<hash>/', views.editor, name='editor'),
    path('<hash>/save/', views.save, name='save')
]