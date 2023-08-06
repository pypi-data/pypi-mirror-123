from report_designer.core.filters import StyledFilterSet, SearchBaseFilterSet


class PatternGroupFilterSet(StyledFilterSet, SearchBaseFilterSet):
    """
    Фильтр: Группы шаблонов
    """

    searching_fields = ('name',)
