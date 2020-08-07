from django.urls import path

from . import views

app_name = 'DbPost'
urlpatterns = [
    path('', views.post_to_database, name='DbPost'),
]