from django.urls import path
from news.views import (
    PostListView,
    PostDetailView,
    PostSearchView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    CategoryListView,
    subscribe,
    unsubscribe,
)

# http://127.0.0.1:8000/news/

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('search/', PostSearchView.as_view(), name='post_search'),
    path('create/', PostCreateView.as_view(), name='news_create'),
    path('articles/create/', PostCreateView.as_view(), name='articles_create'),
    path('<int:pk>/update/', PostUpdateView.as_view(), name='news_update'),
    path('articles/<int:pk>/update/', PostUpdateView.as_view(), name='articles_update'),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name='news_delete'),
    path('articles/<int:pk>/delete/', PostDeleteView.as_view(), name='articles_delete'),
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('subscribe/<int:category_id>/', subscribe, name='subscribe'),
    path('unsubscribe/<int:category_id>/', unsubscribe, name='unsubscribe'),

]
