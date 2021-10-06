from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import News


class ShowNewsView(ListView):
    model = News
    template_name = 'blog/home.html'
    context_object_name = 'news'
    ordering = ['-date']
    paginate_by = 5

    def get_context_data(self, **kwards):
        ctx = super(ShowNewsView, self).get_context_data(**kwards)
        ctx['title'] = 'Главная страница'
        return ctx


class UserAllNewsView(ListView):
    model = News
    template_name = 'blog/user_news.html'
    context_object_name = 'news'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return News.objects.filter(author=user).order_by('-date')


    def get_context_data(self, **kwards):
        ctx = super(UserAllNewsView, self).get_context_data(**kwards)
        ctx['title'] = f"Статьи от пользователя {self.kwargs.get('username')}"
        return ctx


class NewsDetailView(DetailView):
    model = News

    def get_context_data(self, **kwards):
        ctx = super(NewsDetailView, self).get_context_data(**kwards)
        ctx['title'] = News.objects.get(pk=self.kwargs['pk'])
        return ctx


class CreateNewsView(LoginRequiredMixin, CreateView):
    model = News
    template_name = 'blog/create_news.html'
    fields = ['title', 'text']

    def get_context_data(self, **kwards):
        ctx = super(CreateNewsView, self).get_context_data(**kwards)
        ctx['title'] = 'Добавление статьи'
        ctx['btn_text'] = 'Добавить статью'
        return ctx

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class UpdateNewsView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = News
    template_name = 'blog/create_news.html'
    fields = ['title', 'text']

    def get_context_data(self, **kwards):
        ctx = super(UpdateNewsView, self).get_context_data(**kwards)
        ctx['title'] = 'Обновление статьи'
        ctx['btn_text'] = 'Обновить статью'
        return ctx

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        news = self.get_object()
        if self.request.user == news.author:
            return True
        return False


class DeleteNewsView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = News
    success_url = '/'
    template_name = 'blog/news_delete.html'

    def test_func(self):
        news = self.get_object()
        if self.request.user == news.author:
            return True
        return False

def contacts(request):
    return render(request, 'blog/contacts.html', {'title': 'Страница контакты'})
