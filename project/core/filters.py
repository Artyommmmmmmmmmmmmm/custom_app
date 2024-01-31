from django_filters import FilterSet, ModelChoiceFilter
from .models import Comment
from django import forms

class CommentFilter(FilterSet):
    class Meta:
        model = Comment
        fields ={
            'article__title' : ['icontains'],
        }
