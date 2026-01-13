import datetime

from django.contrib.auth.models import User
from django.utils import timezone

from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from news.models import Post, Category


def send_notification(title, preview, pk, subscribers_emails):
    html_content = render_to_string(
        'email/post_created_email.html',
        {
            'link': f'{settings.SITE_URL}/news/{pk}/',
            'preview': preview,
            'title': title,
            'pk': pk
        }
    )
    message = EmailMultiAlternatives(
        subject=title,
        body="",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers_emails,
    )
    message.attach_alternative(html_content, "text/html")
    message.send()


@shared_task
def send_new_post_task(pk):
    post = Post.objects.get(pk=pk)
    categories = post.categories.all()
    subscribers_emails = []

    for category in categories:
        subscribers = category.subscribers.all()
        subscribers_emails += [sub.email for sub in subscribers]

    subscribers_emails = list(set(subscribers_emails))
    send_notification(post.title, post.preview(), post.id, subscribers_emails)


@shared_task
def send_weekly_notification_task():
    daytime_now = timezone.now()
    last_week = daytime_now - datetime.timedelta(days=7)
    posts = Post.objects.filter(created_at__gte=last_week)
    category_names = list(set(posts.values_list('categories__name', flat=True)))
    subscribers_ids = list(
        set(Category.objects.filter(name__in=category_names).values_list('subscribers', flat=True)))

    for subscriber in User.objects.filter(id__in=subscribers_ids):
        subscriber_posts = posts.filter(categories__in=subscriber.categories.all())
        html_content = render_to_string(
            'email/weekly_posts_email.html',
            {
                'link': settings.SITE_URL,
                'username': subscriber.username,
                'posts': list(set(subscriber_posts))
            }
        )
        message = EmailMultiAlternatives(
            subject='Новые посты за последнюю неделю!',
            body="",
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[subscriber.email],
        )
        message.attach_alternative(html_content, "text/html")
        message.send()
