import django
from django.conf import settings

if not settings.configured:
    settings.configure(
        DEBUG=False,
        SECRET_KEY="pyquest-offline-test-key",
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": ":memory:",
            }
        },
        INSTALLED_APPS=[
            "django.contrib.contenttypes",
            "django.contrib.auth",
            "rest_framework",
        ],
        ROOT_URLCONF="views",
        REST_FRAMEWORK={
            "DEFAULT_AUTHENTICATION_CLASSES": [],
            "DEFAULT_PERMISSION_CLASSES": [],
            "UNAUTHENTICATED_USER": None,
        },
        DEFAULT_AUTO_FIELD="django.db.models.BigAutoField",
    )
    django.setup()

from django.db import connection  # noqa: E402
from django.test.utils import CaptureQueriesContext  # noqa: E402
from models import Author, Book  # noqa: E402
from rest_framework.test import APIClient  # noqa: E402

with connection.schema_editor() as schema_editor:
    schema_editor.create_model(Author)
    schema_editor.create_model(Book)


def _reset_tables() -> None:
    Book.objects.all().delete()
    Author.objects.all().delete()


def test_post_creates_book_and_enforces_serializer_validation() -> None:
    _reset_tables()
    author = Author.objects.create(name="Ada Lovelace", country="UK")
    client = APIClient()

    bad_price = client.post(
        "/books/",
        {"title": "Invalid", "isbn": "978-0132350884", "price_cents": -100, "author_id": author.id},
        format="json",
    )
    assert bad_price.status_code == 400
    assert "price_cents" in bad_price.json()

    bad_isbn = client.post(
        "/books/",
        {"title": "Short", "isbn": "123", "price_cents": 1900, "author_id": author.id},
        format="json",
    )
    assert bad_isbn.status_code == 400
    assert "isbn" in bad_isbn.json()

    ok = client.post(
        "/books/",
        {
            "title": "Notes on the Engine",
            "isbn": "978-0132350884",
            "price_cents": 4200,
            "author_id": author.id,
        },
        format="json",
    )
    assert ok.status_code == 201
    body = ok.json()
    assert body["author_name"] == "Ada Lovelace"
    assert body["isbn"] == "9780132350884"


def test_list_books_eliminates_n_plus_one_with_select_related() -> None:
    _reset_tables()
    authors = [Author.objects.create(name=f"Author {i}") for i in range(5)]
    for i in range(15):
        Book.objects.create(
            title=f"Book {i}",
            isbn=f"9780000000{i:03d}",
            price_cents=1500 + i,
            author=authors[i % len(authors)],
        )

    client = APIClient()
    with CaptureQueriesContext(connection) as queries:
        resp = client.get("/books/")

    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 15
    assert data[0]["author_name"] == "Author 0"
    assert len(queries) <= 2, f"Expected <= 2 SQL queries (zero N+1), got {len(queries)}"
