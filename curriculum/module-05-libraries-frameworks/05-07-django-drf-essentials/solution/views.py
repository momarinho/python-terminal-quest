from __future__ import annotations

from django.urls import path
from models import Book
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from serializers import BookSerializer


class BookListCreateView(APIView):
    def get(self, request: Request) -> Response:
        books = Book.objects.select_related("author").order_by("id")
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        serializer = BookSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


urlpatterns = [
    path("books/", BookListCreateView.as_view(), name="book-list-create"),
]
