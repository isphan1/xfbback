from django.contrib import admin
from fb.models import PostReaction, Profile,Message,Comment,Post, RelationShip,SubComment,CommentReaction,SubCommentReaction
from django.db import models
from django.forms import CheckboxSelectMultiple
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):

    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
}

    list_display=['id','user','profile_photo','name']

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display=['id','text','user']
    ordering=["-created_at"]

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display=['id','text']
    ordering=["-created_at"]

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display=['id','text',"sender",'receiver']
    ordering=["-created_at"]

@admin.register(SubComment)
class SubCommentAdmin(admin.ModelAdmin):
    list_display=['id','text','user']
    ordering=["-created_at"]

@admin.register(PostReaction)
class PostReactionAdmin(admin.ModelAdmin):
    list_display = ['type','user','postTitle']

@admin.register(CommentReaction)
class CommentReactionAdmin(admin.ModelAdmin):
    list_display = ['type','user','comment']

@admin.register(SubCommentReaction)
class PostReactionAdmin(admin.ModelAdmin):
    list_display = ['type','user','subComment']

@admin.register(RelationShip)
class RelationshipAdmin(admin.ModelAdmin):
    list_display = ['status','sender','receiver','room']