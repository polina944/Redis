from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from rest_framework.reverse import reverse


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        posts_rating = (
                Post.objects.filter(author=self)
                .aggregate(rating=Sum('rating')).get('rating') or 0
        )
        comments_rating = (
                Comment.objects.filter(user=self.user)
                .aggregate(rating=Sum('rating')).get('rating') or 0
        )
        comments_posts_rating = (
                Comment.objects.filter(post__author=self)
                .aggregate(rating=Sum('rating')).get('rating') or 0
        )

        self.rating = posts_rating * 3 + comments_rating + comments_posts_rating
        self.save()

    def __str__(self):
        return self.user.username


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    subscribers = models.ManyToManyField(User, related_name='categories')

    def __str__(self):
        return self.name


def reversed_lazy(param, kwargs):
    pass


def reverse_lazy(param, kwargs):
    pass


class Post(models.Model):
    news = 'NW'
    articles = 'AR'
    TYPE_CHOICES = (
        (news, 'Новость'),
        (articles, 'Статья')
    )
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=2, choices=TYPE_CHOICES, default=news)
    created_at = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        if len(self.text) <= 124:
            return self.text
        return f'{self.text[: 124]}...'

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
