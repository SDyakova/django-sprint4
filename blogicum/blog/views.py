from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render

from .models import Category
from .utils import get_published_posts


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
