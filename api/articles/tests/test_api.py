import pytest


@pytest.mark.django_db
class TestArticleListCreateAPI:
    url = "/api/v1/articles/"

    def test_list_returns_200(self, api_client):
        response = api_client.get(self.url)
        assert response.status_code == 200

    def test_list_returns_only_published(self, api_client, f):
        f.article(is_published=True)
        f.article(is_published=False)
        response = api_client.get(self.url)
        assert response.data["count"] == 1

    def test_create_returns_201(self, api_client):
        payload = {"user_id": 1, "title": "Test", "content": "Content"}
        response = api_client.post(self.url, payload, format="json")
        assert response.status_code == 201

    def test_create_returns_400_on_invalid_data(self, api_client):
        response = api_client.post(self.url, {}, format="json")
        assert response.status_code == 400


@pytest.mark.django_db
class TestArticleViewAPI:
    def test_view_returns_204(self, api_client, f):
        article = f.article()
        response = api_client.post(f"/api/v1/articles/{article.id}/view/", {"user_id": 1}, format="json")
        assert response.status_code == 204

    def test_view_returns_400_without_user_id(self, api_client, f):
        article = f.article()
        response = api_client.post(f"/api/v1/articles/{article.id}/view/", {}, format="json")
        assert response.status_code == 400

    def test_view_returns_404_for_nonexistent_article(self, api_client):
        response = api_client.post("/api/v1/articles/99999/view/", {"user_id": 1}, format="json")
        assert response.status_code == 404


@pytest.mark.django_db
class TestArticlePopularAPI:
    url = "/api/v1/articles/popular/"

    def test_popular_returns_200(self, api_client):
        response = api_client.get(self.url)
        assert response.status_code == 200

    def test_popular_returns_sorted_by_views(self, api_client, f):
        article1 = f.article(is_published=True)
        article2 = f.article(is_published=True)
        f.article_view(article=article1)
        f.article_view(article=article1)
        f.article_view(article=article2)
        response = api_client.get(self.url)
        assert response.data["results"][0]["id"] == article1.id
