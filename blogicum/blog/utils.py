from django.utils import timezone

from .models import Post


def get_published_posts(queryset=None):
    """
    Возвращает опубликованные посты с pub_date ≤ сейчас.
    Если передан queryset, фильтрация применяется к нему,
    иначе берутся все посты.
    """
    if queryset is None:
        queryset = Post.objects.all()
    return queryset.filter(
        is_published=True,
        pub_date__lte=timezone.now(),
        category__is_published=True,
    ).select_related("category", "location", "author")
