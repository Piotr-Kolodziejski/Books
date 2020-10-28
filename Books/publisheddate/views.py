from django.http import HttpResponse
from django.views import View
import json
import requests
from publisheddate.models import Authors, Book

# Create your views here.


class book_manager(View):
    def get_date(self, book):
        return book['published_date']

    def post(self, request, *args, **kwargs):
        link_string = 'https://www.googleapis.com/books/v1/volumes?q='
        body = json.loads(request.body)
        query = body['q']
        query_string = link_string + query
        response = requests.get(query_string)
        data = json.loads(response.text)
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
            authors = Authors.objects.create(name=authors)
            Book.objects.update_or_create(title=title, book_publish_date=book_publish_date,
                                          defaults={'authors': authors, 'categories': categories,
                                                    'average_rating': average_rating, 
                                                    'ratings_count': ratings_count,
                                                    'thumbnail': thumbnail})
        return HttpResponse("Database updated!")

    def get(self, request, *args, **kwargs):
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
        if kwargs:
            return HttpResponse(json.dumps(books_list[kwargs['book_id']], indent=2), content_type="application/json")

        sort_query = request.GET.get('sort')
        filter_date_query = request.GET.get('published_date')
        filter_authors_query = request.GET.get('author')
        if filter_date_query:
            filtered_date_books_list = []
            for book in books_list:
                if book['published_date'].split('-')[0] == filter_date_query:
                    filtered_date_books_list.append(book)
            return HttpResponse(json.dumps(filtered_date_books_list, indent=2), content_type="application/json")
        if sort_query == 'published_date':
            return HttpResponse(json.dumps(sorted(books_list, key=self.get_date), indent=2), content_type="application/json")
        elif sort_query == '-published_date':
            return HttpResponse(json.dumps(sorted(books_list, key=self.get_date, reverse=True), indent=2), content_type="application/json")
        if filter_authors_query:
            filtered_authors_books_list = []
            for book in books_list:
                if book['authors'][0] == filter_authors_query.replace('"', ''):
                    filtered_authors_books_list.append(book)
            return HttpResponse(json.dumps(filtered_authors_books_list, indent=2), content_type="application/json")
        return HttpResponse(json.dumps(books_list, indent=2), content_type="application/json")
