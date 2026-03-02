from dataclasses import asdict

from articles.models import Article
from articles.transfer_objects.articles import ArticleDTO


def get_all_articles() -> list[dict]:
    articles = Article.objects.filter(is_published=True).only("id", "title", "content", "created_at")
    return [
        asdict(ArticleDTO(id=a.id, title=a.title, content=a.content, created_at=a.created_at.isoformat()))
        for a in articles
    ]
