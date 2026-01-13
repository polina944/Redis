from django_filters import FilterSet, CharFilter, ModelChoiceFilter, DateTimeFilter
from django import forms
from news.models import Author


class PostFilter(FilterSet):
    title = CharFilter(
        field_name='title',
        lookup_expr='iregex',
        label='Заголовок'
    )
    author = ModelChoiceFilter(
        field_name='author',
        queryset=Author.objects.all(),
        label='Автор',
        empty_label='Все авторы'
    )
    created_at = (DateTimeFilter
        (
        field_name='created_at',
        label='Дата позже',
        lookup_expr='gte',
        widget=forms.DateInput(attrs={'type': 'date'})
    ))
