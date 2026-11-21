from __future__ import annotations

from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=120)
    country = models.CharField(max_length=60, default="US")

    class Meta:
        app_label = "contenttypes"


class Book(models.Model):
    title = models.CharField(max_length=200)
    isbn = models.CharField(max_length=32, unique=True)
    price_cents = models.IntegerField()
    author = models.ForeignKey(Author, related_name="books", on_delete=models.CASCADE)

    class Meta:
        app_label = "contenttypes"
