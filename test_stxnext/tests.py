import requests

from django.test import TestCase
from django.urls import reverse

from .importer import Importer


class BookCreateTest(TestCase):

    def test_url_response(self):
        response = self.client.get(reverse('add-book'))
        self.assertEqual(response.status_code, 200, f'expected status code 200, instead get{response.status_code}')

    def test_add_book(self):
        data = {
            "title": "Książka test",
            "published_date": 2022,
            "pages": 123,
            "language": "pl",
            "industry_identifiers-TOTAL_FORMS": 2,
            "industry_identifiers-INITIAL_FORMS": 0,
            "industry_identifiers-MIN_NUM_FORMS": 0,
            "industry_identifiers-0-type": "ISBN",
            "industry_identifiers-0-identifier": "12345678",
            "authors-TOTAL_FORMS": 3,
            "authors-INITIAL_FORMS": 0,
            "authors-MIN_NUM_FORMS": 0,
            "authors-0-author": "Adam",
            "authors-1-author": "Piotr",
            "thumbnails-TOTAL_FORMS": 1,
            "thumbnails-INITIAL_FORMS": 0,
            "thumbnails-MIN_NUM_FORMS": 0,
            "thumbnails-0-small_thumbnail": "https://static.wikia.nocookie.net/zelda/images/0/02/BotW_Link_Shooting_Artwork.png/revision/latest?cb=20170628164822&path-prefix=pl",
            "thumbnails-0-thumbnail": "https://static.wikia.nocookie.net/zelda/images/0/02/BotW_Link_Shooting_Artwork.png/revision/latest?cb=20170628164822&path-prefix=pl",
        }
        response = self.client.post(reverse('add-book'), data)
        self.assertEqual(response.status_code, 302, f'expected status code 302, instead get{response.status_code}')


class AddBookApiTest(TestCase, Importer):
    @classmethod
    def setUpTestData(cls):
        cls.response = requests.get(url="https://www.googleapis.com/books/v1/volumes?q=Hobbit")
        cls.books_json = cls.response.json()
        cls.bookshelf = cls.books_json['items']

    def test_url_response(self):
        response = self.client.get(reverse('add-book-api'))
        self.assertEqual(response.status_code, 200, f'expected status code 200, instead get{response.status_code}')

    def test_search_for_books(self):
        response = self.search_for_books(value="Hobbit")
        self.assertNotEqual(response, None)

    def test_add_title(self):
        for book in self.bookshelf:
            self.assertNotEqual(self.add_title(book), None)

    def test_add_published_date(self):
        for book in self.bookshelf:
            self.assertNotEqual(self.add_published_date(book), None)

    def test_add_pages(self):
        for book in self.bookshelf:
            self.assertNotEqual(book['volumeInfo'].get('pageCount'), None)

    def test_add_language(self):
        for book in self.bookshelf:
            self.assertNotEqual(self.add_language(book), None)

    def test_add_identifiers(self):
        for book in self.bookshelf:
            identifiers = book['volumeInfo'].get('industryIdentifiers')
            self.assertNotEqual(identifiers, None)
            for identifier in identifiers:
                self.assertNotEqual(self.add_identifier(identifier), None)
                self.assertNotEqual(self.add_identifier_type(identifier), None)

    def test_add_author(self):
        for book in self.bookshelf:
            authors = book['volumeInfo'].get('authors')
            self.assertNotEqual(authors, None)
            for author in authors:
                self.assertNotEqual(self.add_author(author), None)

    def test_add_thumbnail(self):
        for book in self.bookshelf:
            self.assertNotEqual(self.add_small_thumbnail(book), None)
            self.assertNotEqual(self.add_thumbnail(book), None)

    def test_google_books_post(self):
        data = {
            'title': "Title",
            'published_date': "2022",
            'pages': "123",
            'language': "en"
        }
        response = self.client.post(reverse('add-book-api'), data)
        self.assertEqual(response.status_code, 302, f'expected status code 302, instead get{response.status_code}')