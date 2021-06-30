from django.db import models
from django.contrib.auth.models import User
import uuid
# Create your models here.

def cover_photo_upload(instance, filename):
    return 'cover/c_{0}/{1}'.format(instance.user.id, filename)

def profile_photo_upload(instance, filename):
    return 'profile/p_{0}/{1}'.format(instance.id, filename)

class Profile(models.Model):  

    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name="profile")
    friends = models.ManyToManyField(User,related_name="friends",blank=True)
    profile_photo = models.ImageField(upload_to=profile_photo_upload)
    cover_photo = models.ImageField(upload_to=cover_photo_upload)
    created_at = models.DateTimeField(auto_now_add=True,null=False)
    updated_at = models.DateTimeField(auto_now=True,null=False)
    id = models.UUIDField(default=uuid.uuid4,  unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return self.user.username

class Post(models.Model):
    
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="posts")
    text = models.CharField(max_length=255,null=False,blank=False)
    created_at = models.DateTimeField(auto_now_add=True,null=False)
    updated_at = models.DateTimeField(auto_now=True,null=False)
    id = models.UUIDField(default=uuid.uuid4,  unique=True,
                          primary_key=True, editable=False)


    def __str__(self) -> str:
        return self.text

class Comment(models.Model):
    
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="comments")
    text = models.CharField(max_length=255,null=False,blank=False)
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