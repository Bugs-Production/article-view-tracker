import pytest
from django.core.cache import cache
from rest_framework.test import APIClient

from articles.tests import factories


class FactoriesProxy:
    def __getattr__(self, attr_name):
        factory_name = "".join(word.capitalize() for word in attr_name.split("_")) + "Factory"
        factory_class = getattr(factories, factory_name, None)
        if factory_class is None:
            raise AttributeError(f"Factory '{factory_name}' not found")
        return factory_class


@pytest.fixture
def f(db):
    return FactoriesProxy()


@pytest.fixture(autouse=True)
def clear_cache():
    cache.clear()
    yield
    cache.clear()


@pytest.fixture
def api_client():
    return APIClient()
