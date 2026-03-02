from rest_framework import serializers


class ArticleCreateSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(min_value=1)
    title = serializers.CharField(max_length=250)
    content = serializers.CharField()


class ArticleViewCreateSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(min_value=1)
