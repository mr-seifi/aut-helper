from django.db import models
from core.models import Student
from uuid import uuid4
from django.contrib.postgres.search import SearchVectorField
from django.contrib.postgres.indexes import GinIndex
from django.utils.text import slugify


class BaseBook(models.Model):
    title = models.TextField(db_index=True)
    authors = models.TextField(db_index=True, null=True)
    publisher = models.TextField(db_index=True, null=True)
    year = models.TextField(null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title} - {self.authors}'


class LibraryBook(BaseBook):
    uid = models.UUIDField(default=uuid4, db_index=True)
    is_exist = models.BooleanField(default=False)
    cover = models.ImageField(upload_to='asset', null=True)


class OnlineBook(models.Model):
    class Languages(models.TextChoices):
        ENGLISH = 'English', 'en'
        RUSSIAN = 'Russian', 'ru'
        FRENCH = 'French', 'fr'
        SPANISH = 'Spanish', 'es'
        GERMAN = 'German', 'de'
        ITALIAN = 'Italian', 'it'

    class Extensions(models.TextChoices):
        PDF = 'pdf', 'PDF'
        EPUB = 'epub', 'EPUB'
        DJVU = 'djvu', 'DJVU'
        DOC = 'doc', 'DOC',
        mobi = 'mobi', 'MOBI',
        rar = 'rar', 'RAR',
        zip = 'zip', 'ZIP'
        azw3 = 'azw3', 'AZW3'

    title = models.TextField(db_index=True)
    authors = models.TextField(db_index=True, null=True)
    publisher = models.TextField(db_index=True, null=True)
    libgen_id = models.IntegerField(unique=True, default=-1)
    slug = models.SlugField(max_length=5000, blank=True)
    description = models.TextField(null=True, blank=True)
    series = models.TextField(null=True, blank=True)
    edition = models.TextField(blank=True)
    pages = models.TextField(null=True, blank=True)
    language = models.CharField(max_length=50, choices=Languages.choices, default=Languages.ENGLISH)
    topic = models.TextField(default='Other')
    cover_url = models.URLField(max_length=2000, null=True, blank=True)
    cover = models.ImageField(upload_to='covers', max_length=5000, null=True, blank=True)
    identifier = models.TextField(blank=True)
    md5 = models.CharField(max_length=300, blank=True)
    filesize = models.IntegerField()
    extension = models.CharField(max_length=50, choices=Extensions.choices, default=Extensions.PDF)
    download_url = models.URLField(max_length=2000, blank=True, null=True)
    file = models.CharField(max_length=50, blank=True, null=True)
    document = SearchVectorField(null=True, blank=True)
    year = models.TextField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['libgen_id']),
            models.Index(fields=['slug']),
            models.Index(fields=['identifier']),
            models.Index(fields=['md5']),
            GinIndex(fields=['document']),
        ]

    def _do_insert(self, manager, using, fields, returning_fields, raw):
        return super(OnlineBook, self)._do_insert(manager,
                                            using,
                                            [f for f in fields if f.attname != 'document'],
                                            returning_fields,
                                            raw)

    def _do_update(self, base_qs, using, pk_val, values, update_fields, forced_update):
        return super(OnlineBook, self)._do_update(base_qs,
                                            using,
                                            pk_val,
                                            [value for value in values if value[0].name != 'document'],
                                            update_fields,
                                            forced_update)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f'{self.title} {self.publisher} {self.year}')
        if self.cover:
            cover_extension = self.cover.name.split('.')[-1]
            self.cover.name = f'{self.slug}.{cover_extension}'
        if self.topic:
            self.topic = slugify(self.topic.replace('\\', ' '))
        self.md5 = self.md5.lower()
        super(OnlineBook, self).save(*args, **kwargs)
