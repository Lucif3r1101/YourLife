from django.shortcuts import render, get_object_or_404
from .models import Post
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.http import HttpResponse
# Create your views here.

'''posts=[
    {
        'author':'Rishav',
        'title':'FirstPost',
        'content':'FirstContent',
        'date_posted':'January 11,2020'
    },
{
        'author':'Lucifer',
        'title':'Second Post',
        'content':'Second Content',
        'date_posted':'January 12,2020'
    }
]'''

def home(request):
    context={
        'posts': Post.objects.all()
    }
    return render(request, 'YourLife/home.html', context)

class PostListView(ListView):
    model=Post
    template_name = 'YourLife/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

class UserPostListView(ListView):
    model=Post
    template_name = 'YourLife/user_posts.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

    def get_queryset(self):
        user=get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model=Post

class PostCreateView(LoginRequiredMixin, CreateView):
    model=Post
    fields=['title' , 'content']

    def form_valid(self, form):
        form.instance.author=self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
    model=Post
    fields=['title' , 'content']

    def form_valid(self, form):
        form.instance.author=self.request.user
        return super().form_valid(form)

    def test_func(self):
        post=self.get_object()
        if self.request.user==post.author:
            return True

class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model=Post
    success_url = '/'

    def test_func(self):
        post=self.get_object()
        if self.request.user==post.author:
            return True
        return False


def about(request):
    return render(request, 'YourLife/about.html',{'title': 'About'})
