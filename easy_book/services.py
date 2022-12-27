import os

from django.conf import settings
from django.db.models import Q
import requests
import pandas as pd
from .models import Book


class BookService:

    def __init__(self):
        self._url = settings.LIBRARY_URL

    def fetch_books(self) -> pd.DataFrame:
        response = requests.get(self._url)
        open('./data/lib.csv', 'wb').write(response.content)

        df = pd.read_csv('data/lib.csv')

        return df

    @classmethod
    def clean_df(cls, df: pd.DataFrame):
        df.drop(axis=1, columns=['اهدایی', 'تعداد نسخ'],
                inplace=True)
        df.rename(columns={'Unnamed: 0': 'title', 'Unnamed: 8': 'status', 'توضیحات': 'description', 'ناشر': 'publisher',
                           'سال': 'year', 'مترجم': 'translator', 'نویسنده': 'author'},
                  inplace=True)
        df.loc[df.status == 'ناموجود', 'status'] = False
        df.loc[df.status == 'موجود', 'status'] = True
        df.index += 1

    @classmethod
    def append_cover_column(cls, df: pd.DataFrame):
        df.insert(
            column='cover',
            loc=7,
            value=''
        )

        assets = {
            i.split('.')[0]: i.split('.')[-1]
            for i in os.listdir('easy_book/asset/')
        }

        for it, row in df.iterrows():
            if str(it) in assets.keys():
                df.loc[it, 'cover'] = f'easy_book/asset/{it}.{assets[str(it)]}'

    @classmethod
    def is_exist(cls, book_series: pd.Series) -> bool:
        return Book.objects.filter(
            title__exact=book_series.title,
            author__exact=book_series.author,
            publisher__exact=book_series.publisher,
            year__exact=book_series.year
        ).exists()

    @classmethod
    def update_status(cls, book_series: pd.Series):
        Book.objects.filter(
            title__exact=book_series.title,
            author__exact=book_series.author,
            publisher__exact=book_series.publisher,
            year__exact=book_series.year
        ).update(
            is_exist=book_series.status
        )

    @classmethod
    def create_book(cls, book_series: pd.Series):
        b = Book(
            title=book_series.title,
            author=book_series.author,
            publisher=book_series.publisher,
            year=book_series.year,
            is_exist=book_series.status,
            cover=book_series.cover.split('/')[-1] if book_series.cover else ''
        )

        b.save()
        if book_series.cover:
            b.cover.save(name=book_series.cover.split('/')[-1], content=open(book_series.cover, 'rb'))
        return b

    @classmethod
    def search_book(cls, query, limit=8):
        return Book.objects.filter(Q(title__icontains=query) |
                                   Q(author__icontains=query) |
                                   Q(publisher__icontains=query)).exclude(title__exact='')[:limit]
