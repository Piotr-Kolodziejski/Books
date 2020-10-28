from django.urls import path

from . import views
from publisheddate.views import book_manager

app_name = 'BookSort'
urlpatterns = [
    #path('', views.SortAndFilter, name='Books'),
    #path('<int:book_id>', views.BookID, name='BookID'),
    path('', book_manager.as_view(), name='Books'),
    path('<int:book_id>', book_manager.as_view(), name='BookID'),
]