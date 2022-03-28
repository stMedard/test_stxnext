from django import forms
from .models import Book, Authors, IndustryIdentifier, Thumbnail
from django.forms.models import inlineformset_factory


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('title', 'publishedDate', 'pageCount', 'language')

class AuthorsForm(forms.ModelForm):
    class Meta:
        model = Authors
        exclude = ()

AuthorsFormSet = inlineformset_factory(
    Book, Authors, form=AuthorsForm, fields=['author', ], extra=3, can_delete=False
)

class IndustryIdentifierForm(forms.ModelForm):
    class Meta:
        model = IndustryIdentifier
        exclude = ()

IndustryIdentifiersFormSet = inlineformset_factory(
    Book, IndustryIdentifier, form=IndustryIdentifierForm,
    fields=['type', 'identifier'], extra=2, can_delete=False
)

class ThumbnailLinkForm(forms.ModelForm):

    class Meta:
        model = Thumbnail
        exclude = ()
        
ThumbnailLinkFormSet = inlineformset_factory(
    Book, Thumbnail, form=ThumbnailLinkForm, fields=['small_thumbnail', 'thumbnail'], extra=1, can_delete=False
)

class SearchBookForm(forms.Form):
    key_word = forms.CharField()