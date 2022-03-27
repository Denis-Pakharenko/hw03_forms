from django.shortcuts import get_object_or_404, render, redirect
from .models import Group, Post, User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .forms import PostForm


POST_COUNT: int = 10


def index(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, POST_COUNT)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = group.posts.all()
    paginator = Paginator(post_list, POST_COUNT)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,
                  'posts/group_list.html',
                  {'group': group,
                   'page_obj': page_obj, }
                  )


def profile(request, username):
    # Здесь код запроса к модели и создание словаря контекста
    author = User.objects.get(username=username)
    posts_author = Post.objects.filter(author=author)
    count = len(posts_author)
    paginator = Paginator(posts_author, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'count': count,
        'author': author,
        'username': username
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post_obj = Post.objects.select_related('author').get(id=post_id)
    author = post_obj.author
    post_count = Post.objects.filter(author=author).count()
    context = {
        'post_obj': post_obj,
        'post_count': post_count
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def create(request):
    is_edit = False
    template = 'posts/create_post.html'
    form = PostForm(request.POST or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('posts:profile', request.user)    
    context = {
        'form': form,
        'is_edit': is_edit
    }
    return render(request, template, context)


@login_required()
def post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    is_edit = True
    template = 'posts/create_post.html'
    if request.user == post.author:
        form = PostForm(request.POST or None, instance=post)
        if form.is_valid():
            form.save()
            return redirect('posts:post_detail', post_id=post_id)
    context = {
        'form': form,
        'is_edit': is_edit,
        'post': post
    }
    return render(request, template, context)
