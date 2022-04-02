from rest_framework import serializers
from articles.models import Article
from django.contrib.auth import get_user_model
User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name'
        )


class ArticleListSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Article
        fields = (
            'id',
            'image',
            'author',
            'title',
            'slug',
            'clean_description',
            'created_on'
        )


class ArticleDetailSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Article
        fields = (
            'id',
            'image',
            'author',
            'title',
            'slug',
            'description',
            'created_on'
        )
