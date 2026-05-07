from django.shortcuts import get_object_or_404, render

from .constants import POSTS_ON_MAIN_PAGE
from .models import Category
from .utils import get_published_posts


def index(request):
    """Главная страница со списком публикаций."""
    post_list = get_published_posts()[:POSTS_ON_MAIN_PAGE]
    return render(request, "blog/index.html", {"post_list": post_list})


def category_posts(request, category_slug):
    """Страница категории."""
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True,
    )
    post_list = get_published_posts(category.posts.all())
    return render(
        request,
        "blog/category.html",
        {
            "category": category,
            "post_list": post_list,
        },
    )


def post_detail(request, post_id):
    """Страница отдельной публикации."""
    post = get_object_or_404(get_published_posts(), pk=post_id)
    return render(request, "blog/detail.html", {"post": post})
