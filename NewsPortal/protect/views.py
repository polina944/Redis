from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from news.models import Post


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'protect/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_author'] = self.request.user.groups.filter(name='authors').exists()
        return context
