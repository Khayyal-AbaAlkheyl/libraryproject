from django.contrib import admin

from .models import Address, Book, Student


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "author", "price", "edition")


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("id", "city")


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "age", "address")
