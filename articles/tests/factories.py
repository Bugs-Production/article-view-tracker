import factory

from articles.models import Article, ArticleView


class ArticleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Article

    user_id = factory.Sequence(lambda n: n + 1)
    title = factory.Sequence(lambda n: f"Article {n}")
    content = factory.Faker("paragraph")
    is_published = True


class ArticleViewFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ArticleView

    article = factory.SubFactory(ArticleFactory)
    user_id = factory.Sequence(lambda n: n + 1)
