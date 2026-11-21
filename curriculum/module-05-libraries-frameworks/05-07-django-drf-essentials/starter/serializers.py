from __future__ import annotations

from models import Author, Book
from rest_framework import serializers


class BookSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source="author.name", read_only=True)
    author_id = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(),
        source="author",
        write_only=True,
    )

    class Meta:
        model = Book
        fields = ["id", "title", "isbn", "price_cents", "author_id", "author_name"]

    def validate_price_cents(self, value: int) -> int:
        # TODO: Reject <= 0 with serializers.ValidationError
        raise NotImplementedError("TODO: validate_price_cents")

    def validate_isbn(self, value: str) -> str:
        # TODO: Reject normalized ISBN shorter than 10 chars with serializers.ValidationError
        raise NotImplementedError("TODO: validate_isbn")
