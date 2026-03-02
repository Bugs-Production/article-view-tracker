from datetime import timedelta

from celery import shared_task
from django.db.models import F
from django.utils import timezone


@shared_task
def increment_views_counter(article_id: int) -> None:
    from articles.models import Article

    Article.objects.filter(id=article_id).update(views_counter=F("views_counter") + 1)


@shared_task
def cleanup_old_article_views() -> None:
    from articles.models import ArticleView

    cutoff = timezone.now() - timedelta(days=30)
    ArticleView.objects.filter(viewed_at__lt=cutoff).delete()
