from celery import shared_task
from django.db.models import F


@shared_task
def increment_views_counter(article_id: int) -> None:
    from articles.models import Article

    Article.objects.filter(id=article_id).update(views_counter=F("views_counter") + 1)
