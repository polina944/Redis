from django import template

register = template.Library()

bed_words = ['редиска', 'дурак']


@register.filter()
def censor(value):
    for word in bed_words:
        value = value.replace(word[1:], '*' * len(word[1:]))

    return value
