from django.urls import path

from api.articles.views import ArticleListCreateView

urlpatterns = [
    path("articles/", ArticleListCreateView.as_view(), name="article-list-create"),
]
