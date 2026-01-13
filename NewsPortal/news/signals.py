from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from news.models import Post
from news.tasks import send_new_post_task


@receiver(m2m_changed, sender=Post.categories.through)
def send_new_post(sender, instance, action, **kwargs):
    if not action == 'post_add':
        return
    send_new_post_task.delay(instance.pk)
