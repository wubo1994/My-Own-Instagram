#from django.shortcuts import render
from annoying.decorators import ajax_request
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from Instagram.models import Post, InstagramUser, Like, Comment, UserConnection
from django.urls import reverse, reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin

from Instagram.forms import CustomUserCreationForm

# Create your views here.
class HelloWorld(TemplateView):
    template_name = 'test.html'

class PostsView(ListView):
    context_object_name = "posts"
    model = Post
    template_name = 'index.html'

class PostDetailView(DetailView):
    model = Post
    template_name = 'detail.html'

class UserProfileView(DetailView):
    model = InstagramUser
    template_name = 'profile.html'

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'create_post.html'
    fields = '__all__' #django magic
    login_url = 'login'

class PostUpdateView(UpdateView):
    model = Post
    template_name = 'update_post.html'
    fields = ['title']

class PostDeleteView(DeleteView):
    model = Post
    template_name = 'delete_post.html'
    success_url = reverse_lazy("posts")

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'sign_up.html'
    success_url = reverse_lazy("login")

@ajax_request
def addLike(request):
    post_pk = request.POST.get('post_pk')
    post = Post.objects.get(pk=post_pk)
    try:
        like = Like(post=post, user=request.user)
        like.save()
        result = 1
    except Exception as e:
        like = Like.objects.get(post=post, user=request.user)
        like.delete()
        result = 0

    return {
        'result': result,
        'post_pk': post_pk
    }

@ajax_request
def addComment(request):
    post_pk = request.POST.get('post_pk')
    comment_text = request.POST.get('comment_text')
    post = Post.objects.get(pk=post_pk)
    try:
        newcomment = Comment(post=post, user=request.user, comment=comment_text)
        newcomment.save()
        result = 1
        comment_info = {
            'username' : request.user.username,
            'comment_text' : comment_text
        }
    except Exception as e:
        result = 0
        comment_info = {
            'username' : request.user.username,
            'comment_text' : comment_text
        }
    return {
        'post_pk' : post_pk,
        'comment_info' : comment_info,
        'result' : result
    }

@ajax_request
def followUnfollow(request):
    print("Beginning of ajax handler.\n")
    be_followed_user_pk = request.POST.get('follow_user_pk')
    follow_unfollow_type = request.POST.get('type')
    following_user_pk = request.user.pk
    be_followed_user = InstagramUser.objects.get(pk=be_followed_user_pk)
    following_user = InstagramUser.objects.get(pk=following_user_pk)
    try:
        if follow_unfollow_type == "follow":
            print("following")
            newconnection = UserConnection(follower=following_user, followee=be_followed_user)
            newconnection.save()
            result = 1
        if follow_unfollow_type == "unfollow":
            print("unfollowing")
            UserConnection.objects.filter(follower=following_user, followee=be_followed_user).delete()
            result = 1
    except Exception as e:
        result = 0
    print("before ajax handler return.\n")
    return {
        'result' : result
    }