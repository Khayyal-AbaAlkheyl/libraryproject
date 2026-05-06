from django.contrib import admin

from .models import Address, Author, Book, PracticeBook, Publisher, Student


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "location")


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "DOB")


@admin.register(PracticeBook)
class PracticeBookAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "author", "price", "edition")


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "price", "quantity", "pubdate", "rating", "publisher")
    list_filter = ("publisher",)
    filter_horizontal = ("authors",)


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("id", "city")


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "age", "address")
