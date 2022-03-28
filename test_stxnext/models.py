from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=75,blank=True,null=True,verbose_name='Tytuł')
    publishedDate = models.CharField(max_length=10,blank=True,null=True,verbose_name='Data publikacji')
    pageCount = models.IntegerField(blank=True,null=True,verbose_name='Ilość stron')
    language = models.CharField(max_length=2,blank=True,null=True,verbose_name='Język')

    class Meta:
        ordering = ('title',)

    def __str__(self):
        return self.title

class Authors(models.Model):
    author = models.CharField(max_length=150,verbose_name='Autor')
    book = models.ForeignKey(Book,on_delete=models.CASCADE,verbose_name='Book',related_name='authors')

    def __str__(self):
        return self.author

class IndustryIdentifier(models.Model):
    type = models.CharField(max_length=25,verbose_name='Typ')
    identifier = models.CharField(max_length=25,verbose_name='Identifikator')
    book = models.ForeignKey(Book,on_delete=models.CASCADE,verbose_name='Book',related_name='industry_identifiers')
    

    def __str__(self):
        return f'{self.type}: {self.identifier}'

class Thumbnail(models.Model):
    small_thumbnail = models.URLField(default=None,blank=True,verbose_name='Small thumbnail')
    thumbnail = models.URLField(default=None,blank=True,verbose_name='Thumbnail')
    book = models.ForeignKey(Book,on_delete=models.CASCADE,verbose_name='Book',related_name='thumbnails')

    def __str__(self):
        return f'{self.small_thumbnail} and {self.thumbnail} from {self.book}'




