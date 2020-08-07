from django.http import HttpResponse
import json
import requests
from dbpost.models import Authors, Book

# Create your views here.

response = requests.get(
    'https://www.googleapis.com/books/v1/volumes?q=war')

data = json.loads(response.text) 
def post_to_database(request):        
    if request.method == "POST":
        body = json.loads(request.body)
        if body == {"q": "war"}:
            for i in data["items"]:
                volumeInfo = i["volumeInfo"]
                title = volumeInfo["title"]
                authors = volumeInfo["authors"]
                book_publish_date = volumeInfo["publishedDate"]
                categories = volumeInfo.get("categories")
                average_rating = volumeInfo.get("averageRating")
                ratings_count = volumeInfo.get("ratingsCount")
                image_links = volumeInfo["imageLinks"]
                thumbnail = image_links["thumbnail"]
                authors = Authors.objects.create(name = authors)
                Book.objects.update_or_create(title = title, book_publish_date = book_publish_date, 
                                            defaults = {'authors': authors, 'categories': categories,
                                                        'average_rating': average_rating, 'ratings_count': ratings_count,
                                                        'thumbnail': thumbnail})
        return HttpResponse("Database updated!")
        
    return HttpResponse("hello")
    

