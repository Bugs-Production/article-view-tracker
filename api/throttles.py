from rest_framework.throttling import AnonRateThrottle


class ArticleViewRateThrottle(AnonRateThrottle):
    scope = "article_view"
