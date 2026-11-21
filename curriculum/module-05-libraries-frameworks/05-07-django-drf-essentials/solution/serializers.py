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
        if value <= 0:
            raise serializers.ValidationError("price_cents must be strictly positive")
        return value

    def validate_isbn(self, value: str) -> str:
        normalized = value.replace("-", "").strip()
        if len(normalized) < 10:
            raise serializers.ValidationError("isbn must contain at least 10 characters")
        return normalized
