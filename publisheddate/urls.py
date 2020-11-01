from django.urls import path

from publisheddate.views import book_manager

app_name = 'BookSort'
urlpatterns = [
    path('', book_manager.as_view(), name='Books'),
    path('<int:book_id>', book_manager.as_view(), name='BookID'),
]