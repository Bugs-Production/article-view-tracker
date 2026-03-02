from django.contrib import admin

from articles.models import Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "user_id", "is_published", "views_counter", "created_at"]
    list_filter = ["is_published"]
    search_fields = ["title", "content"]
    list_editable = ["is_published"]
    readonly_fields = ["views_counter", "created_at", "updated_at"]
