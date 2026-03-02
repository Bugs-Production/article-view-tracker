import pytest

from articles.services.popular_articles import PopularArticlesService


@pytest.mark.django_db
class TestPopularArticlesService:
    def test_returns_list(self):
        service = PopularArticlesService()
        result = service()
        assert isinstance(result, list)

    def test_returns_required_fields(self, f):
        article = f.article()
        f.article_view(article=article)
        service = PopularArticlesService()
        result = service()
        assert len(result) == 1
        item = result[0]
        assert "id" in item
        assert "title" in item
        assert "user_id" in item
        assert "content" in item
        assert "created_at" in item

    def test_sorted_by_views_desc(self, f):
        article1 = f.article()
        article2 = f.article()
        f.article_view(article=article1)
        f.article_view(article=article1)
        f.article_view(article=article2)
        service = PopularArticlesService()
        result = service()
        assert result[0]["id"] == article1.id

    def test_excludes_unpublished(self, f):
        article = f.article(is_published=False)
        f.article_view(article=article)
        service = PopularArticlesService()
        result = service()
        assert len(result) == 0

    def test_uses_cache_on_second_call(self, f):
        f.article_view()
        service = PopularArticlesService()
        result1 = service()
        f.article_view()  # добавляем ещё просмотр — не должен попасть в кеш
        result2 = service()
        assert result1 == result2
