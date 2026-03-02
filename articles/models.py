from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=250)
    content = models.TextField()
    is_published = models.BooleanField(default=False)
    views_counter = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} {self.created_at}"


class ArticleView(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user_id = models.PositiveIntegerField()
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["viewed_at"]),
            models.Index(fields=["article", "viewed_at"]),
        ]

    def __str__(self):
        return f"{self.article} {self.user_id} {self.viewed_at}"
