from rest_framework import mixins, viewsets
from .serializers import ArticleListSerializer, ArticleDetailSerializer
from .filters import ArticleFilter
from articles.models import Article
from django.utils import translation


class ArticleViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    filter_class = ArticleFilter
    lookup_field = "translations__slug"

    def get_serializer_class(self):
        if self.action == 'list':
            return ArticleListSerializer
        if self.action == 'retrieve':
            return ArticleDetailSerializer

    def get_queryset(self):
        language = translation.get_language()
        return Article.objects.translated(language).filter(draft=False,)
