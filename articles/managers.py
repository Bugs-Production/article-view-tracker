from dataclasses import asdict

from articles.models import Article
from articles.transfer_objects.articles import ArticleDTO


def _to_dto(article: Article) -> dict:
    return asdict(
        ArticleDTO(
            id=article.id,
            user_id=article.user_id,
            title=article.title,
            content=article.content,
            created_at=article.created_at.isoformat(),
        )
    )


def create_article(user_id: int, title: str, content: str) -> dict:
    article = Article.objects.create(user_id=user_id, title=title, content=content)
    return _to_dto(article)


def get_all_articles() -> list[dict]:
    articles = Article.objects.filter(is_published=True).only("id", "user_id", "title", "content", "created_at")
    return [_to_dto(a) for a in articles]
