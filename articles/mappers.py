from dataclasses import asdict

from django.db.models import QuerySet

from articles.models import Article
from articles.transfer_objects.articles import ArticleDTO


def articles_to_dict(articles: QuerySet[Article], ordered_ids: list[int]) -> list[dict]:
    articles_map = {
        a.id: asdict(
            ArticleDTO(
                id=a.id,
                user_id=a.user_id,
                title=a.title,
                content=a.content,
                created_at=a.created_at.isoformat(),
                views_counter=a.views_counter,
            )
        )
        for a in articles
    }
    return [articles_map[article_id] for article_id in ordered_ids if article_id in articles_map]
