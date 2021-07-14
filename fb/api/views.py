from django.contrib.auth.models import User
from django.views import generic
from rest_framework.response import Response
from rest_framework.decorators import api_view, schema
from fb.models import Comment, Message, Post, PostReaction, Profile, RelationShip, SubComment
from .serializers import MessageSerializer, PostReactionSerializer, PostSerializer, CommentSerializer, CustomUserTokenSerializer, ProfileSerializer, SubCommentSerializer
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
import json
from django.template.context_processors import csrf
from rest_framework_simplejwt.views import TokenObtainPairView
from django.db.models import Q

url = "http://localhost:8000"
avatarUrl = "http://localhost:8000/media/"


class PostView(ListAPIView, RetrieveModelMixin):

    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):

        u = User.objects.select_related(
            "profile").get(username=request.data['username'])

        post = []

        p = Post.objects.select_related("user").values(
            'text', 'id', 'user__id', 'user__first_name',
            'user__profile__profile_photo', 'created_at'
        ).order_by("-created_at")[:5]

        def postAndComment(x):

            reactions = PostReaction.objects.select_related('post').select_related('user').filter(
                post__id=x['id']).values('id', 'type', 'user__id', 'user__first_name')

            total_reaction = PostReaction.objects.select_related('post').filter(
                post__id=x['id']).count()

            total_comment = Comment.objects.select_related('post').filter(
                post__id=x['id']).count()

            item = {'text': x['text'], 'id': x['id'],
                    'name': x['user__first_name'], 'profile_photo':
                    avatarUrl+x['user__profile__profile_photo'],
                    'created_at': x['created_at'],
                    'total_reaction': total_reaction,
                    'total_comment': total_comment,
                    'reactions': reactions
                    }

            def get_profile_photo(id):
                p = Profile.objects.get(id=id)
                return url+p.profile_photo.url

            c = Comment.objects.select_related("user").select_related("post").filter(
                post__id=x['id']).values("text", "id", 'user__first_name', 'user__profile__id', 'created_at')

            def subCommentAppend(id):

                i = SubComment.objects.select_related("user").select_related(
                    "comment").filter(comment__id=id).values("id", "text", 'user__first_name', 'user__profile__id', 'created_at')

                return [{"text": c['text'], "name":c['user__first_name'], "id":c['id'],
                         'created_at':c['created_at'],
                         'profile_photo':get_profile_photo(c['user__profile__id']),
                         }for c in i]

            comments = [{"text": i['text'], "id":i['id'], 'name':i['user__first_name'],
                         'created_at':i['created_at'],
                         'profile_photo':get_profile_photo(i['user__profile__id']),
                         "subComments":subCommentAppend(i['id'])} for i in c]

            return {"post": item, "comments": comments}

        for x in p.iterator():
            post.append(postAndComment(x))

        return Response(post)


class MessageView(ListAPIView, RetrieveModelMixin):

    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def post(self, request, *args, **kwargs):

        sender = request.data['sender']
        receiver = request.data['receiver']
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
                        "name": x['sender__username'],
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

        msg.sort(key=myFunc, reverse=False)

        return Response(msg)


@api_view(['POST'])
def login(request):

    print("login.........")

    user = authenticate(
        username=request.data['name'], password=request.data['password'])

    if user:
        u = User.objects.get(username=user)
        csrft = str(csrf(request)['csrf_token'])
        return Response({"name": u.username, "id": u.id, "csrf": csrft}, status=200)

    return Response({'msg': "Something went wrong!"}, status=403)


class CustomeUserTokenView(TokenObtainPairView):
    serializer_class = CustomUserTokenSerializer


class AddPost(CreateAPIView, CreateModelMixin):

    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()

    def post(self, request, *args, **kwargs):

        text = request.data['text']
        user = User.objects.get(id=request.data['user_id'])
        id = request.data['id']

        post = Post.objects.create(
            text=text,
            user=user,
            id=id
        )

        return Response({
            "post": {
                "text": text,
                "id": id,
                "name": user.first_name,
                "profile_photo": url+user.profile.profile_photo.url,
                'created_at': post.created_at,
                "total_reaction": 0,
                'total_comment': 0,
                "reactions": []
            },
            "comments": []
        }, status=200)


class RandomPosts(ListAPIView, RetrieveModelMixin):

    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def get(self, request, *args, **kwargs):

        u = User.objects.select_related(
            "profile").get(username="root")

        post = []

        p = Post.objects.prefetch_related("user").values(
            'text', 'id', 'user__id', 'user__first_name',
            'user__profile__profile_photo', 'created_at'
        ).filter(user__username=u.username).order_by('-created_at')[:3]

        def postAndComment(x):

            reactions = PostReaction.objects.select_related('post').select_related('user').filter(
                post__id=x['id']).values('id', 'type', 'user__id', 'user__first_name')

            total_reaction = PostReaction.objects.select_related('post').filter(
                post__id=x['id']).count()

            total_comment = Comment.objects.select_related('post').filter(
                post__id=x['id']).count()

            item = {'text': x['text'], 'id': x['id'],
                    'name': x['user__first_name'], 'profile_photo':
                    avatarUrl+x['user__profile__profile_photo'],
                    'created_at': x['created_at'],
                    'total_reaction': total_reaction,
                    'total_comment': total_comment,
                    'reactions': reactions,
                    }

            def get_profile_photo(id):
                p = Profile.objects.get(id=id)
                return url+p.profile_photo.url

            c = Comment.objects.select_related("user").select_related("post").filter(
                post__id=x['id']).values("text", "id", 'user__first_name', 'user__profile__id', 'created_at')

            def subCommentAppend(id):

                i = SubComment.objects.select_related("user").select_related(
                    "comment").filter(comment__id=id).values("id", "text", 'user__first_name', 'user__profile__id', 'created_at')

                return [{"text": c['text'], "name":c['user__first_name'], "id":c['id'],
                         'created_at':c['created_at'],

                         'profile_photo':get_profile_photo(c['user__profile__id']),
                         }for c in i]

            comments = [{"text": i['text'], "id":i['id'], 'name':i['user__first_name'],
                         'created_at':i['created_at'],
                         'profile_photo':get_profile_photo(i['user__profile__id']),
                         "subComments":subCommentAppend(i['id'])} for i in c]
            return {"post": item, "comments": comments}

        for x in p.iterator():
            post.append(postAndComment(x))

        return Response(post)


class AddComment(CreateAPIView, CreateModelMixin):

    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    queryset = Comment.objects.all()

    def post(self, request, *args, **kwargs):

        text = request.data['text']
        post = Post.objects.get(id=request.data['post_id'])
        user = User.objects.get(id=request.data['user_id'])
        profile = Profile.objects.get(user__id=user.id)
        id = request.data['id']

        comment = Comment.objects.create(
            text=text,
            post=post,
            user=user,
            id=id
        )

        return Response({
            'text': comment.text,
            'user_id': comment.user.id,
            'name': comment.user.first_name,
            'id': comment.id,
            'profile_photo': url+profile.profile_photo.url

        }, status=200)


class AddSubComment(CreateAPIView, CreateModelMixin):

    serializer_class = SubCommentSerializer
    permission_classes = [IsAuthenticated]
    queryset = SubComment.objects.all()

    def post(self, request, *args, **kwargs):

        text = request.data['text']
        comment = Comment.objects.get(id=request.data['comment_id'])
        user = User.objects.get(id=request.data['user_id'])
        profile = Profile.objects.get(user__id=user.id)
        id = request.data['id']

        subComment = SubComment.objects.create(
            text=text,
            comment=comment,
            user=user,
            id=id
        )

        return Response({
            'text': subComment.text,
            'user_id': subComment.user.id,
            'comment_id': comment.id,
            'name': subComment.user.first_name,
            'id': subComment.id,
            'profile_photo': url+profile.profile_photo.url
        }, status=200)


class SearchView(ListAPIView, RetrieveModelMixin):

    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    queryset = Profile.objects.all()

    def post(self, request, *args, **kwargs):

        search = request.data['search']

        r = Profile.objects.select_related("user").filter(
            user__first_name__contains=search).values('id', 'user__first_name', 'profile_photo')

        results = [{'id': i['id'], 'name':i['user__first_name'],
                    'profile_photo':avatarUrl+i['profile_photo']}for i in r]
        return Response(results)


class AddPostReaction(CreateAPIView, CreateModelMixin):

    serializer_class = PostReactionSerializer
    permission_classes = [IsAuthenticated]
    queryset = PostReaction.objects.all()

    def post(self, request, *args, **kwargs):

        type = request.data['type']
        user = User.objects.get(id=request.data['user_id'])
        post = Post.objects.get(id=request.data['post_id'])

        reaction = PostReaction.objects.select_related('post').select_related(
            'user').filter(post__id=post.id).filter(user__id=user.id).first()

        if reaction is None:
            PostReaction.objects.create(
                type=type,
                user=user,
                post=post
            )
        else:

            if reaction.type == type:
                reaction.delete()
            else:
                reaction.type = type
                reaction.save()

        return Response("success")


class AllFriendsListView(ListAPIView, RetrieveModelMixin):

    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):

        id = request.data['user_id']

        u = User.objects.get(id=id)

        s1 = RelationShip.objects.filter(status="REQUEST").filter(
            sender__id=u.id).values('receiver')
        s2 = RelationShip.objects.filter(status="REQUEST").filter(
            receiver__id=u.id).values('sender')

        ss1 = [x['receiver'] for x in s1]
        ss2 = [x['sender'] for x in s2]

        ids = [i.user.id for i in u.friends.all()]

        for x in ss1:
            ids.append(x)

        for x in ss2:
            ids.append(x)

        users = Profile.objects.select_related('user').all().exclude(user__id__in=ids).exclude(user__id=id).values(
            'id', 'profile_photo', 'user__first_name', 'user__id', 'user__username'
        )

        friendlist = []

        def resFriend(x):
            item = {'id': x['id'], 
            'profile_photo': avatarUrl + x['profile_photo'], 
            'user__first_name': x['user__first_name'], 
            'user__id':x['user__id'], 
            'user__username':x['user__username']
            }

            friendlist.append(item)

        for x in users:
            resFriend(x)

        return Response(friendlist)


class PostsList(ListAPIView, RetrieveModelMixin):

    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def get_queryset(self):
        username = self.kwargs['username']
        return Post.objects.filter(user__username=username)


@api_view(['post'])
def sendFriendRequest(request):

    sender = User.objects.get(id=request.data['sender'])
    receiver = User.objects.get(id=request.data['receiver'])

    friend = RelationShip.objects.create(
        sender=sender,
        receiver=receiver,
        status='REQUEST'
    )

    return Response({'msg': "success"}, status=201)


@api_view(['post'])
def accpetFriendRequest(request):

    sender = User.objects.get(id=request.data['sender'])
    receiver = User.objects.get(id=request.data['receiver'])

    accpetRequest = RelationShip.objects.filter(
        sender__id=sender.id).filter(receiver__id=receiver.id).first()

    if accpetRequest.status == "REQUEST":

        accpetRequest.status = "ACCPETED"
        accpetRequest.save()

    return Response({'msg': "success"}, status=201)


class RequestFriendsListView(ListAPIView, RetrieveModelMixin):

    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):

        id = request.data['user_id']

        s1 = RelationShip.objects.filter(status="REQUEST").filter(
            receiver__id=id).values('sender')

        ss1 = [x['sender'] for x in s1]
        users = Profile.objects.select_related('user').filter(user__id__in=ss1).values(
            'id', 'profile_photo', 'user__first_name', 'user__id'
        )

        return Response(users)


class MyFriendsListView(ListAPIView, RetrieveModelMixin):

    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):

        id = request.data['user_id']

        user = User.objects.get(id=id)

        ids = [x.user.id for x in user.friends.all()]

        friends = Profile.objects.select_related('user').filter(user__id__in=ids).values(
            'id', 'profile_photo', 'user__first_name', 'user__id', 'user__username'
        )

        friendlist = []

        def resFriend(x):
            item = {'id': x['id'], 
            'profile_photo': avatarUrl + x['profile_photo'], 
            'user__first_name': x['user__first_name'], 
            'user__id':x['user__id'], 
            'user__username':x['user__username']
            }

            friendlist.append(item)

        for x in friends:
            resFriend(x)

        return Response(friendlist)


@api_view(['post'])
def removeFriend(request):

    user1 = Profile.objects.get(user__id=request.data['user_id'])
    p1 = User.objects.get(id=request.data['id'])

    user2 = Profile.objects.get(user__id=request.data['id'])
    p2 = User.objects.get(id=request.data['user_id'])

    user1.friends.remove(p1)
    user2.friends.remove(p2)

    user1.save()
    user2.save()

    return Response({'msg': "success"}, status=200)


class AddMessageView(CreateAPIView):

    serializer_class = MessageSerializer
    queryset = Message.objects.all()
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):

        sender = User.objects.get(username=request.data['sender'])
        receiver = User.objects.get(username=request.data['receiver'])
        text = request.data['text']
        id = request.data['id']

        Message.objects.create(
            sender=sender,
            receiver=receiver,
            text=text,
            id=id
        )

        return Response({'msg': 'success'}, status=201)


class FriendsMessageList(RetrieveAPIView, RetrieveModelMixin):

    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    permission_classes = [IsAuthenticated]

    def post(self, request):

        sender = request.data['sender']

        f = Profile.objects.select_related("user").get(user__username=sender)
        ids = [x.id for x in f.friends.all()]

        infos = []

        def info(x):

            user = User.objects.get(id=x)

            msg = Message.objects.filter(
                # Q(Q(sender__username=sender) & Q(receiver__id=x)) |
                Q(Q(receiver__username=sender) & Q(sender__id=x))
            ).order_by("-created_at").values('id','text',
            'sender__username','receiver__username','created_at',
            'sender__profile__profile_photo',
            'sender__first_name'
            ).first()

            room = RelationShip.objects.filter(status="ACCPETED").get(
                Q(Q(sender__username=sender) & Q(receiver__id=x)) |
                Q(Q(sender__id=x) & Q(receiver__username=sender))
            )

            infos.append({'msg': {
                'id': msg['id'],
                'text': msg['text'],
                'sender':msg['sender__username'],
                'receiver':msg['receiver__username'],
                'created_at': msg['created_at'],
                'user': {
                    'id': "u1" if sender ==  msg['sender__username'] else "u2",
                    'name': msg['sender__username'],
                    'first_name':msg['sender__first_name'],
                    'profile_photo': avatarUrl +  msg['sender__profile__profile_photo']
                }
            }, 
            'room': room.room,
            'username': user.username
            })

        for x in ids:
            info(x)

        return Response(infos, status=200)
