import django_filters
from .models import Service
from django.db.models import Q

class ServiceFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_search', label="Поиск")
    price__gt = django_filters.NumberFilter(field_name='price', lookup_expr='gt')
    price__lt = django_filters.NumberFilter(field_name='price', lookup_expr='lt')
    order_by = django_filters.OrderingFilter(
        fields=(
            ('name', 'name'),
            ('price', 'price'), 
            ('id', 'newest'),
        ),
        field_labels={
            'name': 'По названию (А-Я)',
            '-name': 'По названию (Я-А)',
            'price': 'По цене (возрастание)',
            '-price': 'По цене (убывание)',
            'newest': 'Новые сначала'
        }
    )

    class Meta:
        model = Service
        fields = []

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value) |
            Q(short_description__icontains=value) |
            Q(full_description__icontains=value)
        )