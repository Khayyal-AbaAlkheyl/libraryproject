from django import forms

from .models import PracticeBook


class PracticeBookForm(forms.ModelForm):
    class Meta:
        model = PracticeBook
        fields = ["title", "author", "price", "edition"]
