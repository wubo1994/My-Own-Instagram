#from django.shortcuts import render
from annoying.decorators import ajax_request
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from Instagram.models import Post, Like
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