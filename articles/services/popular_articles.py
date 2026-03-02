from datetime import timedelta

from django.core.cache import cache
from django.db.models import Count, QuerySet
from django.utils import timezone

from articles.mappers import articles_to_dict
from articles.models import Article, ArticleView


class PopularArticlesService:
    CACHE_KEY = "popular_articles"
    CACHE_TTL = 60 * 5  # 5 минут
    WINDOW_HOURS = 24

    def __call__(self, *args, **kwargs) -> list[dict]:
        cached = cache.get(self.CACHE_KEY)
        if cached is not None:
            return cached

        article_ids = list(self._popular_articles_query())
        result = articles_to_dict(self._articles_query(article_ids), article_ids)

        cache.set(self.CACHE_KEY, result, self.CACHE_TTL)
        return result

    def _popular_articles_query(self) -> QuerySet:
        since = timezone.now() - timedelta(hours=self.WINDOW_HOURS)
        return (
            ArticleView.objects.filter(viewed_at__gte=since)
            .values("article_id")
            .annotate(views_24h=Count("id"))
            .order_by("-views_24h")
            .values_list("article_id", flat=True)
        )

    def _articles_query(self, article_ids: list[int]) -> QuerySet[Article]:
        return Article.objects.filter(id__in=article_ids, is_published=True).only(
            "id", "user_id", "title", "content", "created_at", "views_counter"
        )
