from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Category
from .forms import PostForm

def home(request):
    category_id = request.GET.get('category')
    if category_id:
        posts = Post.objects.filter(category_id=category_id, status='published')
    else:
        posts = Post.objects.filter(status='published')
    categories = Category.objects.all()
    return render(request, "blog/home.html", {"posts": posts, "categories": categories})

def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, "blog/post_form.html", {"form": form, "title": "Create Post"})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = PostForm(instance=post)
    return render(request, "blog/post_form.html", {"form": form, "title": "Edit Post"})

def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        post.delete()
        return redirect('home')
    return render(request, "blog/post_confirm_delete.html", {"post": post})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk, status='published')
    return render(request, "blog/post_detail.html", {"post": post})
