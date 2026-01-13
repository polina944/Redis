from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from news.filters import PostFilter
from news.models import Post, Category
from news.forms import PostForm


class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'news/post_list.html'
    ordering = ['-created_at']
    paginate_by = 10


class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'news/post_detail.html'


class PostSearchView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'news/post_search.html'
    ordering = ['-created_at']
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostCreateView(PermissionRequiredMixin, CreateView):
    model = Post
    template_name = 'news/post_create.html'
    form_class = PostForm
    permission_required = 'news.add_post'

    def form_valid(self, form):
        post = form.save(commit=False)
        if 'articles' in self.request.path:
            post.post_type = 'AR'
        post.author = self.request.user.author
        post.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'articles' in self.request.path:
            context['post_type'] = 'Добавление статьи'
        else:
            context['post_type'] = 'Добавление новости'
        return context


class PostUpdateView(PermissionRequiredMixin, UpdateView):
    model = Post
    template_name = 'news/post_edit.html'
    form_class = PostForm
    success_url = '/news/'
    permission_required = 'news.change_post'


class PostDeleteView(PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'news/post_delete.html'
    success_url = '/news/'
    permission_required = 'news.delete_post'


class CategoryListView(ListView):
    model = Category
    context_object_name = 'categories'
    template_name = 'news/category_list.html'


@login_required
def subscribe(request, category_id):
    category = Category.objects.get(id=category_id)
    user = request.user
    category.subscribers.add(user)
    return redirect(request.META['HTTP_REFERER'])


@login_required
def unsubscribe(request, category_id):
    category = Category.objects.get(id=category_id)
    user = request.user
    category.subscribers.remove(user)
    return redirect(request.META['HTTP_REFERER'])
