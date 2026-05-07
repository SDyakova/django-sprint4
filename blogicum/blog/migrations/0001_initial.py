import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "title",
                    models.CharField(max_length=256, verbose_name="Заголовок"),
                ),
                ("description", models.TextField(verbose_name="Описание")),
                (
                    "slug",
                    models.SlugField(
                        verbose_name="Идентификатор",
                        unique=True,
                        help_text=(
                            "Идентификатор страницы для URL; "
                            "разрешены символы латиницы, цифры, "
                            "дефис и подчёркивание."
                        ),
                    ),
                ),
                (
                    "is_published",
                    models.BooleanField(
                        default=True,
                        verbose_name="Опубликовано",
                        help_text="Снимите галочку, чтобы скрыть категорию.",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Добавлено"),
                ),
            ],
            options={
                "verbose_name": "категория",
                "verbose_name_plural": "Категории",
            },
        ),
        migrations.CreateModel(
            name="Location",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(max_length=256, verbose_name="Название места"),
                ),
                (
                    "is_published",
                    models.BooleanField(default=True, verbose_name="Опубликовано"),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Добавлено"),
                ),
            ],
            options={
                "verbose_name": "местоположение",
                "verbose_name_plural": "Местоположения",
            },
        ),
        migrations.CreateModel(
            name="Post",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "title",
                    models.CharField(max_length=256, verbose_name="Заголовок"),
                ),
                ("text", models.TextField(verbose_name="Текст")),
                (
                    "pub_date",
                    models.DateTimeField(
                        verbose_name="Дата и время публикации",
                        help_text=(
                            "Если установить дату и время в будущем — "
                            "можно делать отложенные публикации."
                        ),
                    ),
                ),
                (
                    "is_published",
                    models.BooleanField(
                        default=True,
                        verbose_name="Опубликовано",
                        help_text="Снимите галочку, чтобы скрыть публикацию.",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Добавлено"),
                ),
                (
                    "author",
                    models.ForeignKey(
                        to=settings.AUTH_USER_MODEL,
                        on_delete=django.db.models.deletion.CASCADE,
                        verbose_name="Автор публикации",
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        to="blog.category",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        verbose_name="Категория",
                    ),
                ),
                (
                    "location",
                    models.ForeignKey(
                        to="blog.location",
                        null=True,
                        blank=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        verbose_name="Местоположение",
                    ),
                ),
            ],
            options={
                "verbose_name": "публикация",
                "verbose_name_plural": "Публикации",
                "ordering": ("-pub_date",),
            },
        ),
    ]
