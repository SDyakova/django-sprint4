from django.db import models
from django.db.models import Count
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect

from .forms import PostForm, UserEditForm, CommentForm
from .models import Category, Post, Comment
from .utils import get_published_posts
from .service import paginate

User = get_user_model()


def index(request):
    """Главная страница со списком публикаций."""
    post_list = get_published_posts()
    page_obj = paginate(post_list, request)
    return render(request, "blog/index.html", {"page_obj": page_obj})


def category_posts(request, category_slug):
    """Страница категории."""
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True,
    )
    post_list = get_published_posts(category.posts.all())
    page_obj = paginate(post_list, request)
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
    if request.user.is_authenticated:
        post = get_object_or_404(
            Post.objects.filter(
                models.Q(is_published=True) | models.Q(author=request.user)
            ),
            pk=post_id,
        )
    else:
        post = get_object_or_404(get_published_posts(), pk=post_id)

    comments = post.comments.filter(is_published=True).select_related("author")
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
    author = get_object_or_404(User, username=username)

    if request.user == author:
        post_list = (
            Post.objects.filter(author=author)
            .annotate(comment_count=Count("comments"))
            .order_by("-pub_date")
        )
    else:
        post_list = get_published_posts(Post.objects.filter(author=author))

    page_obj = paginate(post_list, request)
    return render(
        request,
        "blog/profile.html",
        {
            "profile": author,
            "page_obj": page_obj,
        },
    )


@login_required
def edit_profile(request):
    """Редактирование профиля пользователя."""
    form = UserEditForm(request.POST or None, instance=request.user)
    if form.is_valid():
        form.save()
        return redirect("blog:profile", username=request.user.username)
    return render(request, "blog/user.html", {"form": form})


@login_required
def create_post(request):
    """Создание новой публикации."""
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect("blog:profile", username=request.user.username)
    return render(request, "blog/create.html", {"form": form})


@login_required
def edit_post(request, post_id):
    """Редактирование публикации."""
    post = get_object_or_404(Post, pk=post_id)
    if post.author != request.user:
        return redirect("blog:post_detail", post_id=post_id)

    form = PostForm(request.POST or None, request.FILES or None, instance=post)
    if form.is_valid():
        form.save()
        return redirect("blog:post_detail", post_id=post_id)
    return render(request, "blog/create.html", {"form": form})


@login_required
def delete_post(request, post_id):
    """Удаление публикации."""
    post = get_object_or_404(Post, pk=post_id, author=request.user)
    if request.method == "POST":
        post.delete()
        return redirect("blog:profile", username=request.user.username)
    return render(
        request, "blog/create.html", {"form": PostForm(instance=post)}
    )


@login_required
def add_comment(request, post_id):
    """Добавление комментария."""
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect("blog:post_detail", post_id=post_id)


@login_required
def edit_comment(request, post_id, comment_id):
    """Редактирование комментария."""
    comment = get_object_or_404(
        Comment, pk=comment_id, post__pk=post_id, author=request.user
    )
    form = CommentForm(request.POST or None, instance=comment)
    if form.is_valid():
        form.save()
        return redirect("blog:post_detail", post_id=post_id)
    return render(
        request, "blog/comment.html", {"form": form, "comment": comment}
    )


@login_required
def delete_comment(request, post_id, comment_id):
    """Удаление комментария."""
    comment = get_object_or_404(
        Comment, pk=comment_id, post__pk=post_id, author=request.user
    )
    if request.method == "POST":
        comment.delete()
        return redirect("blog:post_detail", post_id=post_id)
    return render(request, "blog/comment.html", {"comment": comment})
