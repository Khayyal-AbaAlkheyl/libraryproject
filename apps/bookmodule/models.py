from django.db import models
from django.utils import timezone


class Publisher(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=300)

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=200)
    DOB = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField(default=0.0)
    quantity = models.IntegerField(default=1)
    pubdate = models.DateTimeField(default=timezone.now)
    rating = models.SmallIntegerField(default=1)
    publisher = models.ForeignKey(
        Publisher,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="books",
    )
    authors = models.ManyToManyField(Author, blank=True, related_name="books")

    def __str__(self):
        return self.title


class Address(models.Model):
    city = models.CharField(max_length=120)

    class Meta:
        verbose_name_plural = "Addresses"

    def __str__(self):
        return self.city


class Student(models.Model):
    name = models.CharField(max_length=120)
    age = models.PositiveIntegerField()
    address = models.ForeignKey(
        Address,
        on_delete=models.CASCADE,
        related_name="students",
    )

    def __str__(self):
        return self.name


class PracticeBook(models.Model):
    """Lab 7 / Lab 10 CRUD — simple title, author, price, edition (separate from Book)."""

    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    price = models.FloatField(default=0.0)
    edition = models.SmallIntegerField(default=1)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.title
