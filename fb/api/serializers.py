from django.db.models import fields
from fb.models import Comment, Message, Post
from rest_framework.serializers import ModelSerializer

class PostSerializer(ModelSerializer):

    class Meta:
        model = Post
        fields = "__all__"

class CommentSerializer(ModelSerializer):
    
    class Meta:
        model = Comment
        fields = ['text','id']

class MessageSerializer(ModelSerializer):
    
    class Meta:
        model = Message
        fields = ["__all__"]
        depth = 3
