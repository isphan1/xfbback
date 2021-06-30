import os,django

os.environ.setdefault('DJANGO_SETTINGS_MODULE','box.settings')
django.setup()

from fb.models import Post,Comment,SubComment,Message
from django.contrib.auth.models import User
from faker import Faker
import random

def user(n):

    fake = Faker()
    for _ in range(n):
        user = fake.simple_profile()
        profile = User.objects.create(
            username = user['username'],
            first_name = user['name'],
            email = user['mail'],
            is_active = True
        )

        profile.set_password("jnj")
        profile.save()


def post(n):
    fake = Faker()
    user = User.objects.select_related('profile').values('username')
    for _ in n:
        text = fake.sentence(5)
        u = User.objects.get(username = user[random.randint(0,20)]['username'])
        Post.objects.create(
            user = u,
            text = text,
        )

def comment(n):
        fake = Faker()
        user = User.objects.select_related('profile').values('username')
        post = Post.objects.select_related('profile').select_related('comment').values('id')

        u = User.objects.get(username = user[random.randint(0,20)]['username'])
        p = Post.objects.get(id = post[random.randint(0,20)]['id'])
        for _ in n:
    
            text = fake.sentence()
            Comment.objects.create(
                user=u,
                post=p,
                text=text
            )
def subComment(n):
    fake = Faker()
    user = User.objects.select_related('profile').values('username')
    comment = Comment.objects.select_related('profile').select_related('post').values('id')
    
    for _ in n:
        c = Comment.objects.get(text = comment[random.randint(0,500)]['id'])
        u = User.objects.get(username = user[random.randint(0,20)]['username'])
        text = fake.sentence()
        SubComment.objects.create(
            user = u,
            comment = c,
            text = text,
        )

def message(n):

    fake = Faker()
    user = User.objects.select_related('profile').values('username')
    for _ in n:
        u1 = User.objects.get(username = user[random.randint(0,20)]['username'])
        u2 = User.objects.get(username = user[random.randint(0,20)]['username'])
        text = fake.sentence()
        Message.objects.create(
            sender = u1,
            receiver = u2,
            text = text
        )

user(20)
post(500)
comment(2000)
subComment(1000)
message(1000)