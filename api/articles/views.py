from rest_framework.pagination import PageNumberPagination
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from articles.managers import get_all_articles


class ArticleListCreateView(APIView):
    pagination_class = PageNumberPagination

    def get(self, request: Request) -> Response:
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(get_all_articles(), request)
        return paginator.get_paginated_response(page)
