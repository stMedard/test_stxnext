class AddBookApi(Importer):
    search_book_form = SearchBookForm
    book_form = BookForm
    authors_form = AuthorsForm
    identifire_form = IndustryIdentifierForm
    template_name = 'book/add_book_api.html'

    def get(self, request, *args, **kwargs):
        form = self.search_book_form()
        return render(request, self.template_name, {'form': form})

    def search(self, value):
        param = {"q":value}
        books = requests.get(url="https://www.googleapis.com/books/v1/volumes", params=param)
        books_json = books.json()
        if 'items' in books_json:
            bookshelf = books_json['items']
            return bookshelf

    def add_book(self, bookshelf):
        self.object = None
        for book in bookshelf:
            title = self.add_title(book)
            published_date = self.add_published_date(book)
            pages = self.add_pages(book)
            language = self.add_language(book)
            form = self.book_form(
                {'title': title,
                    'published_date': published_date,
                    'pages': pages,
                    'language': language}
            )
            if form.is_valid() and form.cleaned_data["title"] not in Book.objects.values_list('title', flat=True):
                self.object = form.save()
                if book['volumeInfo'].get('authors'):
                    for author in book['volumeInfo']['authors']:
                        author = self.add_author(author)
                        form_author = self.authors_form(
                            {'book': self.object.id, 
                            'author': author}
                        )
                        if form_author.is_valid():
                            form_author.save()
                if book['volumeInfo'].get('industryIdentifiers'):
                    for identifier in book['volumeInfo']['industryIdentifiers']:
                        identifier_type = self.add_identifier_type(identifier)
                        identifier = self.add_identifier(identifier)
                        form_industryidentifier = self.identifire_form(
                            {'book': self.object.id,
                            'type': identifier_type,
                            'identifier': identifier
                                }
                        )
                        if form_industryidentifier.is_valid():
                            form_industryidentifier.save()