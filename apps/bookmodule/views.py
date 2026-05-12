from django.contrib import messages
from django.db.models import (
    Avg,
    Count,
    ExpressionWrapper,
    F,
    FloatField,
    Max,
    Min,
    Q,
    Sum,
    Value,
)
from django.db.models.functions import Coalesce
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PracticeBookForm
from .models import Book, PracticeBook, Publisher, Student


def __getBooksList():
    book1 = {
        "id": 12344321,
        "title": "Continuous Delivery",
        "author": "J.Humble and D. Farley",
    }
    book2 = {
        "id": 56788765,
        "title": "Reversing: Secrets of Reverse Engineering",
        "author": "E. Eilam",
    }
    book3 = {
        "id": 43211234,
        "title": "The Hundred-Page Machine Learning Book",
        "author": "Andriy Burkov",
    }
    return [book1, book2, book3]


def index(request):
    name = request.GET.get("name") or "world!"

    return render(request, "bookmodule/index.html", {"name": name})


def index2(request, val1=0):
    return HttpResponse("value1 = " + str(val1))


def viewbook(request, bookId):
    book1 = {
        "id": 123,
        "title": "Continuous Delivery",
        "author": "J. Humble and D. Farley",
    }
    book2 = {
        "id": 456,
        "title": "Secrets of Reverse Engineering",
        "author": "E. Eilam",
    }
    targetBook = None
    if book1["id"] == bookId:
        targetBook = book1
    if book2["id"] == bookId:
        targetBook = book2
    context = {"book": targetBook}
    return render(request, "bookmodule/show.html", context)


def index(request):
    return render(request, "bookmodule/index.html")


def list_books(request):
    return render(request, "bookmodule/list_books.html")


def viewbook(request, bookId):
    return render(request, "bookmodule/one_book.html")


def aboutus(request):
    return render(request, "bookmodule/aboutus.html")


def html5_links(request):
    return render(request, "bookmodule/html5_links.html")


def html5_text_formatting(request):
    return render(request, "bookmodule/html5_text_formatting.html")


def html5_listing(request):
    return render(request, "bookmodule/html5_listing.html")


def html5_tables(request):
    return render(request, "bookmodule/html5_tables.html")


def search(request):
    if request.method == "POST":
        string = request.POST.get("keyword").lower()
        isTitle = request.POST.get("option1")
        isAuthor = request.POST.get("option2")
        books = __getBooksList()
        newBooks = []
        for item in books:
            contained = False
            if isTitle and string in item["title"].lower():
                contained = True
            if not contained and isAuthor and string in item["author"].lower():
                contained = True
            if contained:
                newBooks.append(item)
        return render(request, "bookmodule/bookList.html", {"books": newBooks})
    return render(request, "bookmodule/search.html")


def simple_query(request):
    mybooks = Book.objects.filter(title__icontains="and")
    return render(request, "bookmodule/bookList.html", {"books": mybooks})


def lookup_query(request):
    mybooks = (
        Book.objects.annotate(_author_count=Count("authors"))
        .filter(_author_count__gt=0)
        .filter(title__icontains="and")
        .filter(rating__gte=2)
        .exclude(price__lte=100)[:10]
    )
    if mybooks.exists():
        return render(request, "bookmodule/bookList.html", {"books": mybooks})
    return render(request, "bookmodule/index.html")


def lab8_task1(request):
    books = Book.objects.filter(Q(price__lte=80))
    return render(
        request,
        "bookmodule/lab8_book_list.html",
        { "books": books},
    )


def lab8_task2(request):
    books = (
        Book.objects.filter(
            Q(rating__gt=3)
            & (Q(title__icontains="qu") | Q(authors__name__icontains="qu"))
        )
        .distinct()
    )
    return render(
        request,
        "bookmodule/lab8_book_list.html",
        {

            "books": books,
        },
    )


def lab8_task3(request):
    combined_q = Q(rating__gt=3) & (
        Q(title__icontains="qu") | Q(authors__name__icontains="qu")
    )
    books = Book.objects.filter(~combined_q).distinct()
    return render(
        request,
        "bookmodule/lab8_book_list.html",
        {
            "books": books,
        },
    )


def lab8_task4(request):
    books = Book.objects.order_by("title").select_related("publisher").prefetch_related(
        "authors"
    )
    return render(
        request,
        "bookmodule/lab8_book_list.html",
        { "books": books},
    )


def lab8_task5(request):
    stats = Book.objects.aggregate(
        book_count=Count("id"),
        total_price=Sum("price"),
        avg_price=Avg("price"),
        max_price=Max("price"),
        min_price=Min("price"),
    )
    return render(
        request,
        "bookmodule/lab8_aggregates.html",
        { "stats": stats},
    )


def lab8_task7(request):
    city_counts = (
        Student.objects.values(city=F("address__city"))
        .annotate(count=Count("id"))
        .order_by("city")
    )
    return render(
        request,
        "bookmodule/lab8_city_counts.html",
        { "city_counts": city_counts},
    )


def lab9_task1(request):

    total_rows = Book.objects.count() or 1
    books = (
        Book.objects.select_related("publisher")
        .prefetch_related("authors")
        .annotate(
            pct_availability=ExpressionWrapper(
                Value(100.0) * F("quantity") / Value(float(total_rows)),
                output_field=FloatField(),
            )
        )
        .order_by("title")
    )
    return render(
        request,
        "bookmodule/lab9_task1.html",
        {"heading": "Lab 9 Task 1 — Availability %", "books": books},
    )


def lab9_task2(request):
    publishers = Publisher.objects.annotate(
        total_stock=Coalesce(Sum("books__quantity"), Value(0))
    ).order_by("name")
    return render(
        request,
        "bookmodule/lab9_task2.html",
        { "publishers": publishers},
    )


def lab9_task3(request):
    rows = []
    for p in Publisher.objects.annotate(oldest_date=Min("books__pubdate")):
        book = None
        if p.oldest_date is not None:
            book = (
                Book.objects.filter(publisher=p, pubdate=p.oldest_date)
                .order_by("id")
                .first()
            )
        rows.append({"publisher": p, "book": book, "oldest_date": p.oldest_date})
    return render(
        request,
        "bookmodule/lab9_task3.html",
        { "rows": rows},
    )


def lab9_task4(request):
    publishers = Publisher.objects.annotate(
        avg_price=Avg("books__price"),
        min_price=Min("books__price"),
        max_price=Max("books__price"),
    ).order_by("name")
    return render(
        request,
        "bookmodule/lab9_task4.html",
        {
            "publishers": publishers,
        },
    )


def lab9_task5(request):
    high = 4
    publishers = Publisher.objects.annotate(
        highly_rated_count=Count("books", filter=Q(books__rating__gte=high)),
        highly_rated_qty=Coalesce(
            Sum("books__quantity", filter=Q(books__rating__gte=high)),
            Value(0),
        ),
    ).order_by("name")
    return render(
        request,
        "bookmodule/lab9_task5.html",
        {

            "publishers": publishers,
            "high_rating_threshold": high,
        },
    )


def lab9_task6(request):
    publishers = Publisher.objects.annotate(
        filtered_book_count=Count(
            "books",
            filter=Q(
                books__price__gt=50,
                books__quantity__gte=1,
                books__quantity__lt=5,
            ),
        )
    ).order_by("name")
    return render(
        request,
        "bookmodule/lab9_task6.html",
        {
            
            "publishers": publishers,
        },
    )


def _practice_parse_edition(post_value):
    if post_value is None or str(post_value).strip() == "":
        return None
    try:
        return int(post_value)
    except (TypeError, ValueError):
        return None


def _practice_parse_price(post_value):
    if post_value is None or str(post_value).strip() == "":
        return None
    try:
        return float(post_value)
    except (TypeError, ValueError):
        return None


def lab10_part1_listbooks(request):
    books = PracticeBook.objects.all()
    return render(request, "bookmodule/lab9_part1_listbooks.html", {"books": books})


def lab10_part1_addbook(request):
    errors = []
    if request.method == "POST":
        title = (request.POST.get("title") or "").strip()
        author = (request.POST.get("author") or "").strip()
        price_raw = request.POST.get("price")
        edition = _practice_parse_edition(request.POST.get("edition"))
        price = _practice_parse_price(price_raw)
        if not title:
            errors.append("Title is required.")
        if not author:
            errors.append("Author is required.")
        if price is None and str(price_raw or "").strip() != "":
            errors.append("Invalid price.")
        if price is None and str(price_raw or "").strip() == "":
            price = 0.0
        if edition is None and str(request.POST.get("edition") or "").strip() != "":
            errors.append("Invalid edition.")
        if edition is None:
            edition = 1
        if errors:
            return render(
                request,
                "bookmodule/lab9_part1_addbook.html",
                {
                    "errors": errors,
                    "title_val": title,
                    "author_val": author,
                    "price_val": price_raw if price_raw is not None else "",
                    "edition_val": request.POST.get("edition") or "",
                },
            )
        PracticeBook.objects.create(
            title=title,
            author=author,
            price=float(price),
            edition=edition,
        )
        messages.success(request, "Book added.")
        return redirect("books.lab10_part1_listbooks")

    return render(request, "bookmodule/lab9_part1_addbook.html", {})


def lab10_part1_editbook(request, id):
    book = get_object_or_404(PracticeBook, pk=id)
    errors = []
    if request.method == "POST":
        title = (request.POST.get("title") or "").strip()
        author = (request.POST.get("author") or "").strip()
        price_raw = request.POST.get("price")
        edition = _practice_parse_edition(request.POST.get("edition"))
        price = _practice_parse_price(price_raw)
        if not title:
            errors.append("Title is required.")
        if not author:
            errors.append("Author is required.")
        if price is None and str(price_raw or "").strip() != "":
            errors.append("Invalid price.")
        if price is None and str(price_raw or "").strip() == "":
            price = 0.0
        if edition is None and str(request.POST.get("edition") or "").strip() != "":
            errors.append("Invalid edition.")
        if edition is None:
            edition = 1
        if errors:
            return render(
                request,
                "bookmodule/lab9_part1_editbook.html",
                {
                    "book": book,
                    "errors": errors,
                    "title_val": title,
                    "author_val": author,
                    "price_val": price_raw if price_raw is not None else "",
                    "edition_val": request.POST.get("edition") or "",
                },
            )
        book.title = title
        book.author = author
        book.price = float(price)
        book.edition = edition
        book.save()
        messages.success(request, "Book updated.")
        return redirect("books.lab10_part1_listbooks")

    return render(
        request,
        "bookmodule/lab9_part1_editbook.html",
        {
            "book": book,
            "title_val": book.title,
            "author_val": book.author,
            "price_val": str(book.price),
            "edition_val": str(book.edition),
        },
    )


def lab10_part1_deletebook(request, id):
    book = get_object_or_404(PracticeBook, pk=id)
    if request.method == "POST":
        book.delete()
        messages.success(request, "Book deleted.")
        return redirect("books.lab10_part1_listbooks")
    return render(
        request,
        "bookmodule/lab9_part1_confirm_delete.html",
        {"book": book},
    )


def lab10_part2_listbooks(request):
    books = PracticeBook.objects.all()
    return render(request, "bookmodule/lab9_part2_listbooks.html", {"books": books})


def lab10_part2_addbook(request):
    if request.method == "POST":
        form = PracticeBookForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Book added.")
            return redirect("books.lab10_part2_listbooks")
    else:
        form = PracticeBookForm()
    return render(
        request,
        "bookmodule/lab9_part2_book_form.html",
        {"form": form, "heading": "Add book (Forms)"},
    )


def lab10_part2_editbook(request, id):
    book = get_object_or_404(PracticeBook, pk=id)
    if request.method == "POST":
        form = PracticeBookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, "Book updated.")
            return redirect("books.lab10_part2_listbooks")
    else:
        form = PracticeBookForm(instance=book)
    return render(
        request,
        "bookmodule/lab9_part2_book_form.html",
        {"form": form, "heading": "Edit book (Forms)"},
    )


def lab10_part2_deletebook(request, id):
    book = get_object_or_404(PracticeBook, pk=id)
    if request.method == "POST":
        book.delete()
        messages.success(request, "Book deleted.")
        return redirect("books.lab10_part2_listbooks")
    return render(
        request,
        "bookmodule/lab9_part2_confirm_delete.html",
        {"book": book},
    )
