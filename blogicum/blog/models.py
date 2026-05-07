from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class PublishedCreatedModel(models.Model):
    """
    Абстрактная модель.
    Добавляет флаги публикации и дату создания.
    """

    is_published = models.BooleanField(
        "Опубликовано",
        default=True,
        help_text="Снимите галочку, чтобы скрыть публикацию.",
    )
    created_at = models.DateTimeField(
        "Добавлено",
        auto_now_add=True,
    )

    class Meta:
        abstract = True


class Category(PublishedCreatedModel):
    title = models.CharField(
        "Заголовок",
        max_length=256,
    )
    description = models.TextField("Описание")
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name="Идентификатор",
        help_text="Идентификатор страницы для URL; "
        "разрешены символы латиницы, цифры, "
        "дефис и подчёркивание.",
    )

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.title[:30]


class Location(PublishedCreatedModel):
    name = models.CharField(
        "Название места",
        max_length=256,
    )

    class Meta:
        verbose_name = "местоположение"
        verbose_name_plural = "Местоположения"

    def __str__(self):
        return self.name[:30]


class Post(PublishedCreatedModel):
    title = models.CharField(
        "Заголовок",
        max_length=256,
    )
    text = models.TextField("Текст")
    pub_date = models.DateTimeField(
        "Дата и время публикации",
        help_text=(
            "Если установить дату и время в будущем — "
            "можно делать отложенные публикации."
        ),
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор публикации",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Категория",
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Местоположение",
    )

    class Meta:
        verbose_name = "публикация"
        verbose_name_plural = "Публикации"
        ordering = ("-pub_date",)
        default_related_name = "posts"

    def __str__(self):
        return self.title[:30]
