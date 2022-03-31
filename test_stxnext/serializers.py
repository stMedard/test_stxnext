from .models import Book
from rest_framework import serializers


class BookSerializer(serializers.ModelSerializer):
    authors_name = serializers.RelatedField(source='authors', read_only=True)
    identifier = serializers.RelatedField(source='industryIdentifier', read_only=True)
    thumbnail = serializers.RelatedField(source='thumbnail', read_only=True)

    class Meta:
        model = Book
        fields = ['id', 'title', 'publishedDate', 'pageCount', 
        'language', 'author_name', 'identifier', 'thumbnail']
