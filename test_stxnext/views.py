from .models import Book, Authors, IndustryIdentifier, Thumbnail
from .forms import ( BookForm, SearchBookForm, IndustryIdentifierForm, AuthorsForm, 
ThumbnailLinkForm, IndustryIdentifiersFormSet, AuthorsFormSet, ThumbnailLinkFormSet )
from .filters import BookFilter
from .importer import Importer
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic import CreateView
from django.views.generic.edit import UpdateView
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import BookSerializer

class BookViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows book to be viewed or edited.
    """
    queryset = Book.objects.all().order_by('-id')
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]


class BookLibraryView(ListView):

    model = Book
    template_name = 'book/book_list.html'
    
    def get_queryset(self, *args, **kwargs):
        book = Book.objects.order_by("-id")
        return book 

def bookListView(request):

    template_name = 'book/book_table.html'

    book_list = Book.objects.order_by("-id")
    myFilter = BookFilter(request.GET, queryset=book_list)
    book_list = myFilter.qs
    context = {'book_list':book_list, 'myFilter':myFilter}
    return render(request, template_name, context)

class BookDetailView(DetailView):

    model = Book
    template_name = 'book/book_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context 
  
class BookCreate(CreateView):
    model = Book
    template_name = 'book/add_book.html'
    form_class = BookForm
    success_url = reverse_lazy('add-book')

    def get(self, request, *args, **kwargs):
        self.object = None
        form = self.form_class()
        identifiers_form = IndustryIdentifiersFormSet
        authors_form = AuthorsFormSet
        thumbnail_form = ThumbnailLinkFormSet
        return self.render_to_response(self.get_context_data(
            form=form,
            identifiers_form=identifiers_form,
            authors_form=authors_form,
            thumbnail_form=thumbnail_form,
        ))

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.form_class(self.request.POST)
        identifiers_form = IndustryIdentifiersFormSet(self.request.POST)
        authors_form = AuthorsFormSet(self.request.POST)
        thumbnail_form = ThumbnailLinkFormSet(self.request.POST)

        if form.is_valid() and identifiers_form.is_valid() and authors_form.is_valid() and thumbnail_form.is_valid():
            return self.form_valid(form, identifiers_form, authors_form, thumbnail_form)
        else:
            return self.form_invalid(form, identifiers_form, authors_form, thumbnail_form)

    def form_valid(self, form, identifiers_form, authors_form, thumbnail_form):
        if form.cleaned_data["title"] not in Book.objects.values_list('title', flat=True):
            self.object = form.save()
            identifiers_form.instance = self.object
            identifiers_form.save()
            authors_form.instance = self.object
            authors_form.save()
            thumbnail_form.instance = self.object
            thumbnail_form.save()

            return HttpResponseRedirect(reverse_lazy('library'))
        else:
            return HttpResponseRedirect(reverse_lazy('add-book'))

    def form_invalid(self, form, identifiers_form, authors_form, thumbnail_form):
        return self.render_to_response(self.get_context_data(
            form=form,
            identifiers_form=identifiers_form,
            authors_form=authors_form,
            thumbnail_form=thumbnail_form,
        ))

class AddBookApi(Importer):
    model = Book
    form_class_book = BookForm
    form_class_search = SearchBookForm
    form_class_identifier = IndustryIdentifierForm
    form_class_author = AuthorsForm
    form_class_thumbnail = ThumbnailLinkForm
    template_name = 'book/add_book_api.html'

    def get(self, request, *args, **kwargs):
        form_2 = self.form_class_search()
        return render(request, self.template_name, {'form_2': form_2})

    def post(self, request, *args, **kwargs):
        self.object = None
        form_2 = self.form_class_search(self.request.POST)
        if form_2.is_valid():
            keyword = form_2.cleaned_data['key_word']
            books = self.search_for_books(keyword)

            if books:
                for book in books:
                    title = self.add_title(book)
                    published_date = self.add_published_date(book)
                    pages = self.add_pages(book)
                    language = self.add_language(book)
                    form = self.form_class_book(
                        {'title': title,
                         'publishedDate': published_date,
                         'pageCount': pages,
                         'language': language}
                    )
                    if form.is_valid() and form.cleaned_data["title"] not in Book.objects.values_list('title', flat=True):
                        self.object = form.save()

                        small_thumbnail = self.add_small_thumbnail(book)
                        thumbnail = self.add_thumbnail(book)
                        form_thumbnail = self.form_class_thumbnail(
                            {'small_thumbnail': small_thumbnail,
                                'thumbnail': thumbnail,
                                'book': self.object.id}
                        )
                        if form_thumbnail.is_valid():
                            form_thumbnail.save()

                        if book['volumeInfo'].get('authors'):
                            for author in book['volumeInfo']['authors']:
                                author = self.add_author(author)
                                form_author = self.form_class_author(
                                    {'author':author,
                                    'book':self.object.id
                                        }
                                )
                                if form_author.is_valid():
                                    form_author.save()

                        if book['volumeInfo'].get('industryIdentifiers'):
                            for identifier in book['volumeInfo']['industryIdentifiers']:
                                identifier_type = self.add_identifier_type(identifier)
                                identifier = self.add_identifier(identifier)
                                form_industryidentifier = self.form_class_identifier(
                                    {'type': identifier_type,
                                        'identifier': identifier,
                                        'book': self.object.id}
                                )
                                if form_industryidentifier.is_valid():
                                    form_industryidentifier.save()

                return HttpResponseRedirect(reverse_lazy('library'))
            else:
                return HttpResponseRedirect(reverse_lazy('add-book-api'))

        else:
            return HttpResponseRedirect(reverse_lazy('add-book-api'))

def delete_book(request, book_id):
    
    book = Book.objects.get(id=book_id)
    book.delete()

    return redirect('library')

class BookEdit(UpdateView):
    model = Book
    template_name = 'book/edit_book.html'
    form_class = BookForm
    identifiers_form = IndustryIdentifiersFormSet
    authors_form = AuthorsFormSet
    thumbnail_form = ThumbnailLinkFormSet
    success_url = reverse_lazy('library')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = Book.objects.get(pk=self.kwargs['pk'])
        context['book'] = book
        context['authors_form'] = self.authors_form(instance=book)
        context['identifiers_form'] = self.identifiers_form(instance=book)
        context['thumbnail_form'] = self.thumbnail_form(instance=book)

        return context

    def post(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        book = Book.objects.get(pk = pk)
        book_form = self.form_class(instance=book, data=request.POST)
        authors_form = self.authors_form(instance=book, data=request.POST)
        identifiers_form = self.identifiers_form(instance=book, data=request.POST)
        thumbnail_form = self.thumbnail_form(instance=book, data=request.POST)

        if book_form.is_valid() and identifiers_form.is_valid() and authors_form.is_valid() and thumbnail_form.is_valid():
            return self.form_valid(book_form, identifiers_form, authors_form, thumbnail_form)
        else:
            return self.form_invalid(book_form, identifiers_form, authors_form, thumbnail_form)

    def form_valid(self, book_form, identifiers_form, authors_form, thumbnail_form):
        if book_form.cleaned_data["title"]:
            self.object = book_form.save()
            identifiers_form.instance = self.object
            identifiers_form.save()
            authors_form.instance = self.object
            authors_form.save()
            thumbnail_form.instance = self.object
            thumbnail_form.save()

            return HttpResponseRedirect(reverse_lazy('library'))
        else:
            return HttpResponseRedirect(reverse_lazy('edit-book'))

    def form_invalidd(self, form, identifiers_form, authors_form, thumbnail_form):
        return self.render_to_response(self.get_context_data(
            form=form,
            identifiers_form=identifiers_form,
            authors_form=authors_form,
            thumbnail_form=thumbnail_form,
        ))