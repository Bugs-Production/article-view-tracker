import logging
from dataclasses import asdict

from articles.models import Article, ArticleView
from articles.tasks import increment_views_counter
from articles.transfer_objects.articles import ArticleDTO

logger = logging.getLogger("articles")


def _to_dto(article: Article) -> dict:
    return asdict(
        ArticleDTO(
            id=article.id,
            user_id=article.user_id,
            title=article.title,
            content=article.content,
            created_at=article.created_at.isoformat(),
            views_counter=article.views_counter,
        )
    )


def create_article_view(article_id: int, user_id: int) -> None:
    ArticleView.objects.create(article_id=article_id, user_id=user_id)
    increment_views_counter.delay(article_id)
    logger.info("Article view recorded: article_id=%s user_id=%s", article_id, user_id)


def create_article(user_id: int, title: str, content: str) -> dict:
    article = Article.objects.create(user_id=user_id, title=title, content=content)
    logger.info("Article created: id=%s user_id=%s", article.id, user_id)
    return _to_dto(article)


def get_all_articles() -> list[dict]:
    articles = Article.objects.filter(is_published=True).only(
        "id", "user_id", "title", "content", "created_at", "views_counter"
    )
    return [_to_dto(a) for a in articles]
