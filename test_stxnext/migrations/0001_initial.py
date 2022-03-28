# Generated by Django 4.0.3 on 2022-03-26 16:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=75, null=True, verbose_name='Tytuł')),
                ('publishedDate', models.CharField(blank=True, max_length=10, null=True, verbose_name='Data publikacji')),
                ('pageCount', models.IntegerField(blank=True, null=True, verbose_name='Ilość stron')),
                ('language', models.CharField(blank=True, max_length=2, null=True, verbose_name='Język')),
            ],
            options={
                'ordering': ('title',),
            },
        ),
        migrations.CreateModel(
            name='Thumbnail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('small_thumbnail', models.URLField(blank=True, default=None, verbose_name='Small thumbnail')),
                ('thumbnail', models.URLField(blank=True, default=None, verbose_name='Thumbnail')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='thumbnails', to='test_stxnext.book', verbose_name='Book')),
            ],
        ),
        migrations.CreateModel(
            name='IndustryIdentifier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=25, verbose_name='Typ')),
                ('identifier', models.CharField(max_length=25, verbose_name='Identifikator')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='industry_identifiers', to='test_stxnext.book', verbose_name='Book')),
            ],
        ),
        migrations.CreateModel(
            name='Authors',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=150, verbose_name='Autor')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='authors', to='test_stxnext.book', verbose_name='Book')),
            ],
        ),
    ]