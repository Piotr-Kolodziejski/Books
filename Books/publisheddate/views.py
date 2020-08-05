from django.shortcuts import render
from django.http import HttpResponse
import json
import requests

# Create your views here.

response = requests.get(
    'https://www.googleapis.com/books/v1/volumes?q=Hobbit')

books_list = []
data = json.loads(response.text)
for i in data["items"]:
    volumeInfo = i["volumeInfo"]
    title = volumeInfo["title"]
    authors = volumeInfo["authors"]
    published_date = volumeInfo["publishedDate"]
    categories = volumeInfo.get("categories")
    average_rating = volumeInfo.get("averageRating")
    ratings_count = volumeInfo.get("ratingsCount")
    image_links = volumeInfo["imageLinks"]
    thumbnail = image_links["thumbnail"]
    books_list.append({'title': title, 'authors': authors, 'published_date': published_date,
                       'categories': categories, 'average_rating': average_rating,
                       'ratings_count': ratings_count, 'thumbnail': thumbnail, })


def get_date(book):
    return book['published_date']


def SortAndFilter(request):
    sort_query = request.GET.get('sort')
    filter_date_query = request.GET.get('published_date')
    filter_authors_query = request.GET.get('author')
    print(books_list[1])
    if filter_date_query:
        filtered_date_books_list = []
        for book in books_list:
            if book['published_date'].split('-')[0] == filter_date_query:
                filtered_date_books_list.append(book)
        return HttpResponse(json.dumps(filtered_date_books_list, indent=2), content_type="application/json")
    if sort_query == 'published_date':
        return HttpResponse(json.dumps(sorted(books_list, key=get_date), indent=2), content_type="application/json")
    elif sort_query == '-published_date':
        return HttpResponse(json.dumps(sorted(books_list, key=get_date, reverse=True), indent=2), content_type="application/json")
    if filter_authors_query:
        filtered_authors_books_list = []
        for book in books_list:
            if book['authors'][0] == filter_authors_query.replace('"', ''):
                filtered_authors_books_list.append(book)
        return HttpResponse(json.dumps(filtered_authors_books_list, indent=2), content_type="application/json")
    return HttpResponse(json.dumps(books_list, indent=2), content_type="application/json")

def BookID(request, book_id):
    return HttpResponse(json.dumps(books_list[book_id], indent=2), content_type="application/json")
    
