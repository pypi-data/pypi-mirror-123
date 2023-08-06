from report_designer.core.filters import StyledFilterSet, SearchBaseFilterSet
from report_designer.models import Pattern, PatternField


class PatternFilterSet(StyledFilterSet, SearchBaseFilterSet):
    """
    Фильтр: Шаблоны
    """

    searching_fields = ('name',)
    searching_select = (
        'root',
        'author',
    )

    class Meta:
        model = Pattern
        fields = (
            'root',
            'author',
            'groups',
        )


class PatternFieldsFilterSet(StyledFilterSet, SearchBaseFilterSet):
    """
    Фильтр: Поля таблицы шаблона
    """

    searching_fields = (
        'alias',
        'name',
    )
    searching_select = ('representation',)

    class Meta:
        model = PatternField
        fields = (
            'is_virtual',
            'is_group',
            'is_sort',
            'reverse_sort',
            'is_aggregate',
        )
