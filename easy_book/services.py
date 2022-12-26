import os

from django.conf import settings
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
                df.loc[it, 'cover'] = f'asset/{it}.{assets[str(it)]}'

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
        return Book.objects.create(
            title=book_series.title,
            author=book_series.author,
            publisher=book_series.publisher,
            year=book_series.year,
            is_exist=book_series.status,
            cover=book_series.cover or None
        )
