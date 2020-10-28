from django.http import HttpResponse
from django.views import View
import json
import requests
from publisheddate.models import Authors, Book

# Create your views here.


class book_manager(View):
    def __init__(self):
        response = requests.get(
            'https://www.googleapis.com/books/v1/volumes?q=Hobbit')

        self.books_list = []
        self.data = json.loads(response.text)

    def get_date(self, book):
        return book['published_date']

    def post(self, request, *args, **kwargs):
        if request.body == {"q": "war"}:
            for i in self.data["items"]:
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
        for i in self.data["items"]:
            volumeInfo = i["volumeInfo"]
            title = volumeInfo["title"]
            authors = volumeInfo["authors"]
            published_date = volumeInfo["publishedDate"]
            categories = volumeInfo.get("categories")
            average_rating = volumeInfo.get("averageRating")
            ratings_count = volumeInfo.get("ratingsCount")
            image_links = volumeInfo["imageLinks"]
            thumbnail = image_links["thumbnail"]
            self.books_list.append({'title': title, 'authors': authors, 'published_date': published_date,
                                    'categories': categories, 'average_rating': average_rating,
                                    'ratings_count': ratings_count, 'thumbnail': thumbnail, })
        if self.kwargs:
            return HttpResponse(json.dumps(self.books_list[self.kwargs['book_id']], indent=2), content_type="application/json")

        sort_query = request.GET.get('sort')
        filter_date_query = request.GET.get('published_date')
        filter_authors_query = request.GET.get('author')
        if filter_date_query:
            filtered_date_books_list = []
            for book in self.books_list:
                if book['published_date'].split('-')[0] == filter_date_query:
                    filtered_date_books_list.append(book)
            return HttpResponse(json.dumps(filtered_date_books_list, indent=2), content_type="application/json")
        if sort_query == 'published_date':
            return HttpResponse(json.dumps(sorted(self.books_list, key=self.get_date), indent=2), content_type="application/json")
        elif sort_query == '-published_date':
            return HttpResponse(json.dumps(sorted(self.books_list, key=self.get_date, reverse=True), indent=2), content_type="application/json")
        if filter_authors_query:
            filtered_authors_books_list = []
            for book in self.books_list:
                if book['authors'][0] == filter_authors_query.replace('"', ''):
                    filtered_authors_books_list.append(book)
            return HttpResponse(json.dumps(filtered_authors_books_list, indent=2), content_type="application/json")
        return HttpResponse(json.dumps(self.books_list, indent=2), content_type="application/json")
