from django.shortcuts import render
from django.http import HttpResponse
from .models import Comment, Post, SubComment, User
import json
# Create your views here.

def index(request):

    u = User.objects.select_related('profile').first()

    p = Post.objects.select_related("user").filter(user=u).first()

    c = Comment.objects.select_related("user").select_related("post").filter(post__id=p.id).values('text',"id",'created_at').order_by("?")

    sc = SubComment.objects.select_related("user").select_related("comment").filter(comment__id=c[0]['id'])


    context = {
        "post":p,
        "comments":[{"comment":c,
        "subComments":sc,
        }]
    }
    data = json.dumps(context, indent=4, sort_keys=True, default=str)
    return HttpResponse(data, content_type='application/json')
