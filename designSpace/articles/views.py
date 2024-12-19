from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from designSpace.accounts.models import Profile
from designSpace.articles.forms import ArticleForm
from designSpace.articles.models import Article
from designSpace.articles.permissions import IsArticleOwner
from designSpace.articles.serializers import ArticleSerializer


class ArticleViewSet(ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated, IsArticleOwner]

class ArticleCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'articles/create-article.html'
    login_url = reverse_lazy('log-in')

    def get_success_url(self):
        return reverse_lazy('profile-articles', kwargs={'pk': self.request.user.pk})

    def form_valid(self, form):
        form.instance.author = self.request.user

        return super().form_valid(form)

    def test_func(self):
        return self.request.user.groups.filter(name='Writer').exists()

    def handle_no_permission(self):
        messages.error(self.request, "You do not have permission to create articles.")
        return redirect(reverse('profile-details', args=[self.request.user.id]))

    def get_login_url(self):
        return f"{reverse_lazy('log-in')}?next={self.request.path}"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_pk'] = self.request.user.pk

        return context


class ArticleDetailsView(LoginRequiredMixin, DetailView):
    model = Article
    template_name = 'articles/article-details.html'
    context_object_name = 'article'

    def get_object(self, queryset=None):
        return get_object_or_404(Article, pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        article = self.get_object()

        profile_user = get_object_or_404(Profile, user=article.author)
        context['profile'] = profile_user

        context['is_author'] = self.request.user == article.author

        return context


class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'articles/article-edit.html'
    login_url = reverse_lazy('log-in')

    def get_success_url(self):
        return reverse_lazy('articles:article-details', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        article = self.get_object()
        return article.author == self.request.user or self.request.user.groups.filter(name='Writer').exists()

    def handle_no_permission(self):
        messages.error(self.request, "You do not have permission to edit this article.")
        return redirect('home')

    def get_login_url(self):
        return f"{reverse_lazy('log-in')}?next={self.request.path}"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_pk'] = self.request.user.pk
        return context


class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Article
    template_name = 'articles/article-delete.html'
    login_url = reverse_lazy('log-in')

    def get_success_url(self):
        return reverse_lazy('profile-articles', kwargs={'pk': self.request.user.pk})

    def test_func(self):
        article = self.get_object()
        return article.author == self.request.user or self.request.user.groups.filter(name='Writer').exists()

    def handle_no_permission(self):
        messages.error(self.request, "You do not have permission to delete this article.")
        return redirect('home')

    def get_login_url(self):
        return f"{reverse_lazy('log-in')}?next={self.request.path}"