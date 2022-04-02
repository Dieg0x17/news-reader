import django_filters
from django.db.models import Q
from django_filters import DateFilter

from articles.models import Article


class ArticleFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_search')
    start_date = DateFilter(field_name='created_on', lookup_expr='gte')
    end_date = DateFilter(field_name='created_on', lookup_expr='lte')
    order = django_filters.CharFilter(method='filter_order')

    class Meta:
        model = Article
        fields = ('created_on',)

    def filter_search(self, queryset, value, *args, **kwargs):
        filter_value = args[0]
        return queryset.filter(
            Q(translations__description__icontains=filter_value) |
            Q(translations__title__icontains=filter_value) |
            Q(translations__slug__icontains=filter_value) |
            Q(author__first_name__icontains=filter_value) |
            Q(author__last_name__icontains=filter_value)
        ).distinct()

    def filter_order(self, queryset, value, *args, **kwargs):
        order = args[0]
        if order == "recent":
            return queryset.order_by("-created_on")
        if order == "old":
            return queryset.order_by("created_on")
        return queryset
