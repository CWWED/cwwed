import django_filters

from named_storms.models import NsemPsaData


class NsemPsaFilter(django_filters.FilterSet):
    variable = django_filters.CharFilter(field_name='nsem_psa_variable', lookup_expr='name')

    class Meta:
        model = NsemPsaData
        fields = {
            'value': ['exact', 'gt', 'gte', 'lt', 'lte'],
            'date': ['exact'],
        }
