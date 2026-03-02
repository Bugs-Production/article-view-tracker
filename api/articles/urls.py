from django.urls import path

from api.articles.views import ArticleListCreateView, ArticlePopularListView, ArticleViewCreateView

urlpatterns = [
    path("articles/", ArticleListCreateView.as_view(), name="article-list-create"),
    path("articles/popular/", ArticlePopularListView.as_view(), name="article-popular-list"),
    path("articles/<int:article_id>/view/", ArticleViewCreateView.as_view(), name="article-view-create"),
]
