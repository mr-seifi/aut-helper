# Generated by Django 4.1.4 on 2022-12-30 10:51

import django.contrib.postgres.indexes
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('easy_book', '0002_onlinebook_document'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='onlinebook',
            index=django.contrib.postgres.indexes.GinIndex(fields=['document'], name='easy_book_o_documen_575611_gin'),
        ),
    ]
