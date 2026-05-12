from django.db.models import Count
from django.utils import timezone

from .models import Post


def get_published_posts(queryset=None):
    """
    Возвращает опубликованные посты с pub_date ≤ сейчас.

    Если передан queryset, фильтрация применяется к нему,
    иначе берутся все посты.
    """
    queryset = queryset or Post.objects.all()
    return (
        queryset.filter(
            is_published=True,
            pub_date__lte=timezone.now(),
            category__is_published=True,
            location__is_published=True,
        )
        .annotate(comment_count=Count("comments"))
        .select_related("author", "location", "category")
        .order_by("-pub_date")
    )
