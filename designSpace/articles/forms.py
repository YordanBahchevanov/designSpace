from django import forms

from designSpace.articles.models import Article


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        exclude = ('author', 'slug',)