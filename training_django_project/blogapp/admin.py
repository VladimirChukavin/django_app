from django.contrib import admin

from .models import Article


@admin.register(Article)
class ArticlesAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "content",
        "pub_date",
        "author__name",
        "category__name",
    )
    list_display_links = ("id", "title")
    ordering = ("id",)
    search_fields = ("title", "content", "pub_date", "author__name", "category__name")
