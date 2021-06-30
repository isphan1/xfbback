from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.decorators import api_view, schema
from fb.models import Comment, Message, Post, SubComment
from .serializers import MessageSerializer, PostSerializer, CommentSerializer
from rest_framework.generics import ListAPIView
from rest_framework.mixins import RetrieveModelMixin
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
import json
from django.template.context_processors import csrf


class PostView(ListAPIView, RetrieveModelMixin):

    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):

        u = User.objects.select_related(
            "profile").get(username=request.data['username'])

        post = []

        p = Post.objects.prefetch_related("user").values(
            'text', 'id').order_by("?").filter(user__id=u.id)[:3]

        def postAndComment(x):

            c = Comment.objects.select_related("user").select_related("post").filter(
                post__id=x['id']).values("text", "id", 'user__first_name')

            def subCommentAppend(id):

                i = SubComment.objects.select_related("user").select_related(
                    "comment").filter(comment__id=id).values("id", "text", 'user__first_name')

                return [{"text": c['text'], "name":c['user__first_name'], "id":c['id']}for c in i]

            comments = [{"text": i['text'], "id":i['id'], 'name':i['user__first_name'],
                         "subComments":subCommentAppend(i['id'])} for i in c]

            return {"post": x, "comments": comments}

        for x in p.iterator():
            post.append(postAndComment(x))

        return Response(post)


class MessageView(ListAPIView, RetrieveModelMixin):

    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def get(self, request, *args, **kwargs):

        sender = kwargs['user1']
        receiver = kwargs['user2']
        msg = []

        m1 = Message.objects.filter(sender__username=sender).filter(
            receiver__username=receiver).values('id', 'text', 'sender__username', 'receiver__username', 'created_at')
        m2 = Message.objects.filter(receiver__username=sender).filter(
            sender__username=receiver).values('id', 'text', 'sender__username', 'receiver__username', 'created_at')

        def addMsg(item):
            for x in item:
                if sender == x['sender__username']:
                    msg.append({'id': x['id'], 'text': x['text'], 'created_at': x['created_at'], 'user': {
                        "id": "u1",
                        "name": x['sender__username']
                    }})
                else:
                    msg.append({'id': x['id'], 'text': x['text'], 'created_at': x['created_at'], 'user': {
                        "id": "u2",
                        "name": x['sender__username']
                    }})

        addMsg(m1)
        addMsg(m2)

        def myFunc(e):
            return e['created_at']

        msg.sort(key=myFunc)

        return Response(msg)


@api_view(['POST'])
def login(request):

    print("login.........")

    user = authenticate(username=request.data['name'],password=request.data['password'])

    if user:
        u = User.objects.get(username=user)
        csrft = str(csrf(request)['csrf_token'])
        return Response({"name":u.username,"id":u.id,"csrf":csrft},status=201)

    return Response({'msg':"Something went wrong!"},status=403)
