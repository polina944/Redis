import datetime
import logging

from django.conf import settings
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth.models import User

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from news.models import Post, Category

logger = logging.getLogger(__name__)


# наша задача по выводу текста на экран
def my_job():
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
    print('Рассылка завершена!')


# функция, которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            my_job,
            trigger=CronTrigger(second="*/1"),
            # То же, что и интервал, но задача тригера таким образом более понятна django
            id="my_job",  # уникальный айди
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
