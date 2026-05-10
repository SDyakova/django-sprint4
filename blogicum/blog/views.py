from django.db.models import Count
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone

from .forms import PostForm, UserEditForm, CommentForm
from .models import Category, Post, Comment
from .utils import get_published_posts

User = get_user_model()


def index(request):
    """Главная страница со списком публикаций."""
    post_list = get_published_posts()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "blog/index.html", {"page_obj": page_obj})


def category_posts(request, category_slug):
    """Страница категории."""
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True,
    )
    post_list = get_published_posts(category.posts.all())
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(
        request,
        "blog/category.html",
        {
            "category": category,
            "page_obj": page_obj,
        },
    )


def post_detail(request, post_id):
    """Страница отдельной публикации."""
    post = get_object_or_404(Post, pk=post_id)

    if not post.category.is_published:
        if request.user != post.author:
            raise Http404("Пост не найден")

    if not post.is_published or post.pub_date > timezone.now():
        if request.user != post.author:
            raise Http404("Пост не найден")

    comments = post.comments.filter(is_published=True)
    form = CommentForm()
    return render(
        request,
        "blog/detail.html",
        {
            "post": post,
            "comments": comments,
            "form": form,
        },
    )


def profile(request, username):
    """Страница пользователя."""
    user = get_object_or_404(User, username=username)
    post_list = (
        Post.objects.filter(author=user)
        .annotate(comment_count=Count("comments"))
        .order_by("-pub_date")
    )
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(
        request,
        "blog/profile.html",
        {
            "profile": user,
            "page_obj": page_obj,
        },
    )


@login_required
def edit_profile(request):
    """Редактирование профиля пользователя."""
    if request.method == "POST":
        form = UserEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("blog:profile", username=request.user.username)
    else:
        form = UserEditForm(instance=request.user)
    return render(request, "blog/user.html", {"form": form})


@login_required
def create_post(request):
    """Создание новой публикации."""
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("blog:profile", username=request.user.username)
    else:
        form = PostForm()
    return render(request, "blog/create.html", {"form": form})


@login_required
def edit_post(request, post_id):
    """Редактирование публикации."""
    post = get_object_or_404(Post, pk=post_id)
    if post.author != request.user:
        return redirect("blog:post_detail", post_id=post_id)

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect("blog:post_detail", post_id=post_id)
    else:
        form = PostForm(instance=post)

    return render(request, "blog/create.html", {"form": form})


@login_required
def delete_post(request, post_id):
    """Удаление публикации."""
    post = get_object_or_404(Post, pk=post_id)
    if post.author != request.user:
        return redirect("blog:post_detail", post_id=post_id)

    if request.method == "POST":
        post.delete()
        return redirect("blog:profile", username=request.user.username)

    return render(request, "blog/create.html", {"post": post})


@login_required
def add_comment(request, post_id):
    """Добавление комментария."""
    post = get_object_or_404(Post, pk=post_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
    return redirect("blog:post_detail", post_id=post_id)


@login_required
def edit_comment(request, post_id, comment_id):
    """Редактирование комментария."""
    post = get_object_or_404(Post, pk=post_id)
    comment = get_object_or_404(Comment, pk=comment_id, post=post)

    if comment.author != request.user:
        return redirect("blog:post_detail", post_id=post_id)

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect("blog:post_detail", post_id=post_id)
    else:
        form = CommentForm(instance=comment)

    return render(
        request, "blog/comment.html", {"form": form, "comment": comment}
    )


@login_required
def delete_comment(request, post_id, comment_id):
    """Удаление комментария."""
    post = get_object_or_404(Post, pk=post_id)
    comment = get_object_or_404(Comment, pk=comment_id, post=post)

    if comment.author != request.user:
        return redirect("blog:post_detail", post_id=post_id)

    if request.method == "POST":
        comment.delete()
        return redirect("blog:post_detail", post_id=post_id)

    return render(request, "blog/comment.html", {"comment": comment})
