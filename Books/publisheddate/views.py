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
    books_list.append(json.dumps({'title': title, 'authors': authors, 'published_date': published_date,
                                    'categories': categories, 'average_rating': average_rating,
                                    'ratings_count': ratings_count, 'thumbnail': thumbnail, }, indent = 2))
    
books = {}
for i in range(10):
    books[i] = json.loads(books_list[i])

def PublishedDate(request):
    return HttpResponse(json.dumps(books, indent = 2), content_type="application/json")
