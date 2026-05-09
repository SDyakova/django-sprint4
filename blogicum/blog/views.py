from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render, redirect

from .forms import PostForm, UserEditForm
from .models import Category
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
    post = get_object_or_404(get_published_posts(), pk=post_id)
    return render(request, "blog/detail.html", {"post": post})


def profile(request, username):
    """Страница пользователя."""
    user = get_object_or_404(User, username=username)
    post_list = get_published_posts().filter(author=user)
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
