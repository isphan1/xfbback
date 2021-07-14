from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("",views.RandomPosts.as_view()),
    path("posts/",views.PostView.as_view()),
    path("postslist/<str:username>",views.PostsList.as_view()),
    path("search/",views.SearchView.as_view()),
    
    path("friends/",views.AllFriendsListView.as_view()),
    path("friendsrequest/",views.RequestFriendsListView.as_view()),
    path("myfriendsrequest/",views.MyFriendsListView.as_view()),
    path("sendrequest/",views.sendFriendRequest),
    path("accpetrequest/",views.accpetFriendRequest),
    path("removefriend/",views.removeFriend),

    path("postreaction/",views.AddPostReaction.as_view()),
    path('addpost/',views.AddPost.as_view()),
    path('addcomment/',views.AddComment.as_view()),
    path('addsubcomment/',views.AddSubComment.as_view()),
    path("login/",views.login),

    path("message/",views.MessageView.as_view()),
    path("addmessage/",views.AddMessageView.as_view()),
    path("getmessageinfo/",views.FriendsMessageList.as_view()),


    path('token/', views.CustomeUserTokenView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),


]
