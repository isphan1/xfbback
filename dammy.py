import os,django

os.environ.setdefault('DJANGO_SETTINGS_MODULE','box.settings')
django.setup()

from fb.models import Post,Comment,SubComment,Message
from django.contrib.auth.models import User
from faker import Faker
import random

def dammy(n):

    user = User.objects.select_related('profile').values('username')
    post = Post.objects.select_related('profile').select_related('comment').values('text')
    comment = Comment.objects.select_related('profile').select_related('post').values('text')
    fake = Faker()


    for _ in range(n):
    #     user = fake.simple_profile()

    #     profile = User.objects.create(
    #         username = user['username'],
    #         first_name = user['name'],
    #         email = user['mail'],
    #         is_active = True
    #     )

    #     profile.set_password("jnj")
    #     profile.save()

        text = fake.sentence()
        s = User.objects.get(username = user[random.randint(0,20)]['username'])
        r = User.objects.get(username = user[random.randint(0,20)]['username'])
        # c = Comment.objects.get(text = comment[random.randint(0,530)]['text'])
        # SubComment.objects.create(
        #     user = u,
        #     comment = c,
        #     text = text,
        # )

        Message.objects.create(
            sender = s,
            receiver = r,
            text = text
        )

dammy(200)