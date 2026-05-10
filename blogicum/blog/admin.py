from django.contrib import admin
from django.utils.html import format_html

from .models import Category, Comment, Location, Post


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "is_published", "created_at")
    list_editable = ("is_published",)
    search_fields = ("title",)
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("name", "is_published", "created_at")
    list_editable = ("is_published",)
    search_fields = ("name",)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "author",
        "category",
        "location",
        "pub_date",
        "is_published",
        "image_preview",
    )
    list_display_links = ("title", "author")
    list_editable = ("is_published",)
    list_filter = ("category", "location", "is_published")
    search_fields = ("title", "text")
    date_hierarchy = "pub_date"

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "title",
                    "text",
                    ("pub_date", "image"),
                    ("category", "location"),
                    "is_published",
                )
            },
        ),
        (
            "Автор",
            {
                "fields": ("author",),
            },
        ),
    )

    readonly_fields = ("image_preview",)

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 50px; width: auto;" />',
                obj.image.url,
            )
        return "Нет изображения"

    image_preview.short_description = "Превью"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("text", "author", "post", "created_at", "is_published")
    list_editable = ("is_published",)
    list_filter = ("is_published", "author", "created_at")
    search_fields = ("text", "author__username", "post__title")
