import random
from .models import Post, Category

post_types = ['NW', 'AR']

authors_ids = [1, 2]


def gen_post():
    for i in range(4, 51):
        kwargs = {
            "author_id": random.choice(authors_ids),
            "post_type": random.choice(post_types),
            "title": f"Заголовок поста {i}",
            "text": f"Содержание поста {i}"
        }

        Post.objects.create(**kwargs)
    print("Все посты успешно созданы!")

# def update_post_1():
#     for i in range(1, 9):
#         post = Post.objects.get(pk=i)
#         post.title_en = f"Title post {i}"
#         post.text_en = f"Content post {i}"
#         post.save()
#     print("Все посты успешно изменены!")
#
# def update_post_2():
#     for i in range(11, 51):
#         post = Post.objects.get(pk=i)
#         post.title_en = f"Title post {i}"
#         post.text_en = f"Content post {i}"
#         post.save()
#     print("Все посты успешно изменены!")
#
#
# def update_category():
#     categories = ['Sports', 'Technology', 'Music', 'Politics', 'Economics', 'Space', 'Art', 'Cinema']
#     for i, v in enumerate(categories):
#         category = Category.objects.get(pk=i + 1)
#         category.name_en = v
#         category.save()
#     print("Все категории успешно изменены!")
