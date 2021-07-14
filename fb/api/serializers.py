from django.contrib.auth.models import User
from rest_framework import serializers
from fb.models import Comment, Message, Post, PostReaction, SubComment,Profile
from rest_framework.serializers import HyperlinkedModelSerializer, ModelSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class ProfileSerializer(ModelSerializer):
    
    class Meta:
        model = Profile
        fields = "__all__"
        depth = 3

class SubCommentSerializer(ModelSerializer):
    class Meta:
        model = SubComment
        fields = "__all__"

class CommentSerializer(ModelSerializer):
    subComments = SubCommentSerializer(many=True)
    class Meta:
        model = Comment
        fields = ['id','text','created_at','subComments']


class PostSerializer(ModelSerializer):
    
    comments = CommentSerializer(many=True)
    class Meta:
        model = Post
        fields = ['id','text','user','comments'] 
        depth = 3

class MessageSerializer(ModelSerializer):
    
    class Meta:
        model = Message
        fields = ["__all__"]
        depth = 3

class PostReactionSerializer(ModelSerializer):
    
    class Meta:
        model = PostReaction
        fields = "__all__"
        depth = 2


class CustomUserTokenSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # custom fields add in TokenObtainPairSerializer package file

        return token
