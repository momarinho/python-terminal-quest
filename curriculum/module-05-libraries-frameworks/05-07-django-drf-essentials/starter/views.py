from __future__ import annotations

from django.urls import path
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class BookListCreateView(APIView):
    def get(self, request: Request) -> Response:
        # TODO: Query Book.objects.select_related("author").order_by("id") and return serialized JSON
        raise NotImplementedError("TODO: BookListCreateView.get")

    def post(self, request: Request) -> Response:
        # TODO: Validate with BookSerializer, save and return 201 Created (or 400 Bad Request)
        raise NotImplementedError("TODO: BookListCreateView.post")


urlpatterns = [
    path("books/", BookListCreateView.as_view(), name="book-list-create"),
]
