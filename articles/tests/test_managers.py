import pytest

from articles.managers import create_article, create_article_view, get_all_articles
from articles.models import ArticleView


@pytest.mark.django_db
class TestGetAllArticles:
    def test_returns_list(self, f):
        f.article()
        result = get_all_articles()
        assert isinstance(result, list)
        assert len(result) == 1

    def test_returns_required_fields(self, f):
        f.article()
        result = get_all_articles()
        article = result[0]
        assert "id" in article
        assert "user_id" in article
        assert "title" in article
        assert "content" in article
        assert "created_at" in article
        assert "views_counter" in article

    def test_excludes_unpublished(self, f):
        f.article(is_published=False)
        result = get_all_articles()
        assert len(result) == 0


@pytest.mark.django_db
class TestCreateArticle:
    def test_returns_required_fields(self):
        result = create_article(user_id=1, title="Test", content="Content")
        assert "id" in result
        assert "user_id" in result
        assert "title" in result
        assert "content" in result
        assert "created_at" in result

    def test_creates_in_db(self):
        from articles.models import Article

        create_article(user_id=1, title="Test", content="Content")
        assert Article.objects.count() == 1


@pytest.mark.django_db
class TestCreateArticleView:
    def test_creates_view_in_db(self, f):
        article = f.article()
        create_article_view(article_id=article.id, user_id=1)
        assert ArticleView.objects.filter(article=article).count() == 1
