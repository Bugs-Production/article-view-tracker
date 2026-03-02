from django.urls import include, path

urlpatterns = [
    path("", include("api.articles.urls")),
]
