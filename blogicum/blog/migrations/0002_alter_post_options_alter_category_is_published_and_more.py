from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="post",
            options={
                "default_related_name": "posts",
                "ordering": ("-pub_date",),
                "verbose_name": "публикация",
                "verbose_name_plural": "Публикации",
            },
        ),
        migrations.AlterField(
            model_name="category",
            name="is_published",
            field=models.BooleanField(
                default=True,
                help_text="Снимите галочку, чтобы скрыть публикацию.",
                verbose_name="Опубликовано",
            ),
        ),
        migrations.AlterField(
            model_name="category",
            name="slug",
            field=models.SlugField(
                help_text="Идентификатор страницы для URL. "
                "Разрешены символы латиницы, цифры, дефис и подчёркивание.",
                unique=True,
                verbose_name="Идентификатор",
            ),
        ),
        migrations.AlterField(
            model_name="location",
            name="is_published",
            field=models.BooleanField(
                default=True,
                help_text="Снимите галочку, чтобы скрыть публикацию.",
                verbose_name="Опубликовано",
            ),
        ),
    ]
