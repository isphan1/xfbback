from django.db import models
from django.contrib.auth.models import User
import uuid

from django.db.models.base import Model
# Create your models here.

import random
import string

def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str



def cover_photo_upload(instance, filename):
    return 'cover/c_{0}/{1}'.format(instance.user.id, filename)

def profile_photo_upload(instance, filename):
    return 'profile/p_{0}/{1}'.format(instance.id, filename)

class Profile(models.Model):  

    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name="profile")
    friends = models.ManyToManyField(User,related_name="friends",blank=True)
    profile_photo = models.ImageField(default="a.png",upload_to=profile_photo_upload,blank=True)
    cover_photo = models.ImageField(default="w.jpg",upload_to=cover_photo_upload,blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=False)
    updated_at = models.DateTimeField(auto_now=True,null=False)
    id = models.UUIDField(default=uuid.uuid4,  unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return self.user.username
    
    @property
    def name (self):
        return self.user.first_name

class Post(models.Model):
    
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="posts")
    text = models.TextField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True,null=False)
    updated_at = models.DateTimeField(auto_now=True,null=False)
    id = models.UUIDField(default=uuid.uuid4,  unique=True,
                          primary_key=True, editable=False)


    def __str__(self):
        return self.text

class Comment(models.Model):
    
    text = models.CharField(max_length=255,null=False,blank=False)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="comments")
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name="comments")
    created_at = models.DateTimeField(auto_now_add=True,null=False)
    updated_at = models.DateTimeField(auto_now=True,null=False)
    id = models.UUIDField(default=uuid.uuid4,  unique=True,
                          primary_key=True, editable=False)

    def __str__(self) -> str:
        return self.text

class SubComment(models.Model):
    
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="subComments")
    text = models.CharField(max_length=255,null=False,blank=False)
    comment = models.ForeignKey(Comment,on_delete=models.CASCADE,related_name="subComments")
    created_at = models.DateTimeField(auto_now_add=True,null=False)
    updated_at = models.DateTimeField(auto_now=True,null=False)
    id = models.UUIDField(default=uuid.uuid4,  unique=True,
                          primary_key=True, editable=False)
    def __str__(self) -> str:
        return self.text

class Message(models.Model):

    sender = models.ForeignKey(User,on_delete=models.CASCADE,related_name="s1")
    receiver = models.ForeignKey(User,on_delete=models.CASCADE,related_name="r1")
    text = models.CharField(max_length=255,null=False,blank=False)
    created_at = models.DateTimeField(auto_now_add=True,null=False)
    updated_at = models.DateTimeField(auto_now=True,null=False)
    id = models.UUIDField(default=uuid.uuid4,  unique=True,
                          primary_key=True, editable=False)

    @property
    def sender_info(self):
        return self.created_at

    def __str__(self) -> str:
        return self.text

class PostReaction(models.Model):
        REACTION = (
        ('LIKE','LIKE'),
        ('LOVE','LOVE'),
        ('HAHA','HAHA'),
        ('ANGRY','ANGRY'),
        ('SAD','SAD'),
        ('WOW','WOW'))

        type = models.CharField(choices=REACTION,default="LIKE",blank=False,max_length=10)
        user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="post_reactions")
        post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name="post_reactions")
    
        def __str__(self):
            return self.type
        

        @property
        def postTitle(self):
            return self.post.text
            

class CommentReaction(models.Model):
        REACTION = (
        ('LIKE','LIKE'),
        ('LOVE','LOVE'),
        ('HAHA','HAHA'),
        ('ANGRY','ANGRY'),
        ('SAD','SAD'),
        ('WOW','WOW'))

        type = models.CharField(choices=REACTION,default="LIKE",blank=False,max_length=10)
        user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="comment_reactions")
        comment = models.ForeignKey(Post,on_delete=models.CASCADE,related_name="comment_reactions")
    
class SubCommentReaction(models.Model):
        REACTION = (
        ('LIKE','LIKE'),
        ('LOVE','LOVE'),
        ('HAHA','HAHA'),
        ('ANGRY','ANGRY'),
        ('SAD','SAD'),
        ('WOW','WOW'))

        type = models.CharField(choices=REACTION,default="LIKE",blank=False,max_length=10)
        user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="subComment_reactions")
        subComment = models.ForeignKey(Post,on_delete=models.CASCADE,related_name="subcComment_reactions")
    

class RelationShip(models.Model):

    status_choice = (
        ('REQUEST','REQUEST'),
        ('ACCPETED','ACCPETED')
    )

    sender = models.ForeignKey(User,on_delete=models.CASCADE,related_name="r_sender")
    receiver = models.ForeignKey(User,on_delete=models.CASCADE,related_name="r_receiver")
    status = models.TextField(choices=status_choice,default="REQUEST",blank=False)
    room = models.CharField(default=get_random_string(8),max_length=8,blank=False)
    id = models.UUIDField(default=uuid.uuid4,  unique=True,
                          primary_key=True, editable=False)