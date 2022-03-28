import django_filters
from django_filters import DateFilter
from .models import Book

class BookFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name='publishedDate', lookup_expr='gte')
    end_date = DateFilter(field_name='publishedDate', lookup_expr='lte')
    class Meta:
        model = Book
        fields = ('title', 'authors', 'publishedDate', 'language')
        exclude = ['publishedDate']