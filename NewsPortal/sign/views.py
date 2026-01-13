from django.contrib.auth.models import User
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from .forms import BaseRegisterForm
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required

from news.models import Author


@login_required
def set_authors(request):
    user = request.user
    premium_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        premium_group.user_set.add(user)
    Author.objects.get_or_create(user=user)
    return redirect('/profile/')


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/sign/login/'


class ConfirmLogout(TemplateView):
    template_name = 'sign/logout.html'
