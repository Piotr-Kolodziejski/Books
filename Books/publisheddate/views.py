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


def PublishedDate(request):
    query = request.GET.get('published_date')
    if query:
        filtered_books_list = []
        for book in books_list:
            if book['published_date'].split('-')[0] == query:
                filtered_books_list.append(book)
        return HttpResponse(json.dumps(filtered_books_list, indent=2), content_type="application/json")
    return HttpResponse(json.dumps(books_list, indent=2), content_type="application/json")
