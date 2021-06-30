from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Comment, Post, SubComment 
import json
# Create your views here.


def index(request):

        u = User.objects.select_related(
        "profile").get(username="root")

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

        return HttpResponse(post, content_type='application/json')
