from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post, Comment, Tag
from .forms import PostForm, CommentForm, TagForm
from django.contrib.auth.decorators import login_required
from django.db.models import Count

# Create your views here.


def post_list(request):
    tag_filter = arr_to_str(request.POST.getlist('tag'))
    result_query = request.POST.get('q')

    
    if result_query or tag_filter:
        if result_query and tag_filter:
            posts = Post.objects.filter(published_date__lte=timezone.now(), title__contains=result_query, tag_search__contains=tag_filter)
            result_count = Post.objects.filter(published_date__lte=timezone.now(), title__contains=result_query, tag_search__contains=tag_filter).aggregate(Count('title'))
            tag = Tag.objects.all()
        elif result_query:
            posts = Post.objects.filter(published_date__lte=timezone.now(), title__contains=result_query)
            result_count = Post.objects.filter(published_date__lte=timezone.now(), title__contains=result_query).aggregate(Count('title'))
            tag = Tag.objects.all()
        elif tag_filter:
            posts = Post.objects.filter(published_date__lte=timezone.now(), tag_search__contains=tag_filter)
            result_count = Post.objects.filter(published_date__lte=timezone.now(), tag_search__contains=tag_filter).aggregate(Count('title'))
            tag = Tag.objects.all()
    else:
        posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
        tag = Tag.objects.all()
        result_count = 0
    return render(request, 'blog/post_list.html', {'posts': posts, 'result_count': result_count, 'tags': tag})

@login_required
def tag_list(request):
    tags = Tag.objects.all()
    return render(request, 'blog/tag_list.html', {'tags': tags})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            tag_filter = request.POST.getlist('tag')
            tags = []
            print(tag_filter)
            for tag in tag_filter:
                result_tag = Tag.objects.get(id=tag)
                tags.append(result_tag.title)
            
            post = form.save(commit=False)
            post.author = request.user
            post.tag_search = arr_to_str(tags)
            # post.published_date = timezone.now() //tutorial-extension
            post.save()

            form.save_m2m()

            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def arr_to_str(s):
    str1 = " "
    return (str1.join(s))

@login_required
def tag_new(request):
    if request.method == "POST":
        form = TagForm(request.POST)
        if form.is_valid():
            tag = form.save(commit=False)
            tag.save()
            return redirect('tag_list')
    else:
        form = TagForm()
    return render(request, 'blog/tag_edit.html', {'form': form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            tag_filter = request.POST.getlist('tag')
            tags = []
            print(tag_filter)
            for tag in tag_filter:
                result_tag = Tag.objects.get(id=tag)
                tags.append(result_tag.title)
            
            post = form.save(commit=False)
            post.author = request.user
            post.tag_search = arr_to_str(tags)
            # post.published_date = timezone.now() //tutorial-extension
            post.save()
            form.save_m2m()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)

@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')

def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})

@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.post.pk)

