from django.urls import path

from . import views

app_name = 'BookSort'
urlpatterns = [
    path('', views.SortAndFilter, name='Books'),
    path('<int:book_id>', views.BookID, name='BookID'),
]