from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from api.articles.serializers import ArticleCreateSerializer, ArticleViewCreateSerializer
from articles.managers import create_article, create_article_view, get_all_articles
from articles.services.popular_articles import PopularArticlesService


class ArticleListCreateView(APIView):
    pagination_class = PageNumberPagination

    def get(self, request: Request) -> Response:
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(get_all_articles(), request)
        return paginator.get_paginated_response(page)

    def post(self, request: Request) -> Response:
        serializer = ArticleCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(create_article(**serializer.validated_data), status=status.HTTP_201_CREATED)


class ArticlePopularListView(APIView):
    pagination_class = PageNumberPagination

    def get(self, request: Request) -> Response:
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(PopularArticlesService()(), request)
        return paginator.get_paginated_response(page)


class ArticleViewCreateView(APIView):
    def post(self, request: Request, article_id: int) -> Response:
        serializer = ArticleViewCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        create_article_view(article_id=article_id, user_id=serializer.validated_data["user_id"])
        return Response(status=status.HTTP_204_NO_CONTENT)
