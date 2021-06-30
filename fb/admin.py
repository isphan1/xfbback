from django.contrib import admin
from fb.models import Profile,Message,Comment,Post,SubComment
# Register your models here.

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display=['id','user','profile_photo']

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display=['id','text','user']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display=['id','text']

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display=['id','text',"sender",'receiver']

@admin.register(SubComment)
class SubCommentAdmin(admin.ModelAdmin):
    list_display=['id','text','user']