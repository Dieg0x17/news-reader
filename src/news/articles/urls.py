from django.urls import path, include
from .views import Index
from .feeds import RSS, Atom
from rest_framework.routers import DefaultRouter
from articles.api.viewsets import ArticleViewSet

router = DefaultRouter()
router.register('articles', ArticleViewSet, 'articles')

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('rss', RSS(), name="rss"),
    path('atom', Atom(), name="atom"),
    path('', include(router.urls))
]
