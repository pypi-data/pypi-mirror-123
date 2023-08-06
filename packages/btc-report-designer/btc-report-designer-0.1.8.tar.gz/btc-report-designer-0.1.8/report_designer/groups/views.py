from report_designer.core.views import (
    BreadcrumbsListMixin,
    DynamicContentTableBaseView,
    UpdateAjaxView,
    CreateAjaxView,
)
from report_designer.groups.actions import PatternGroupListActionGroup
from report_designer.groups.filters import PatternGroupFilterSet
from report_designer.groups.forms import PatternGroupCreateUpdateForm
from report_designer.groups.tables import PatternGroupTable
from report_designer.models import PatternGroup


# region Базовые миксины


class PatternGroupBreadcrumbsListMixin(BreadcrumbsListMixin):
    """
    Хлебные крошки групп шаблонов
    """

    title_breadcrumb = 'Список групп шаблонов'


# endregion Базовые миксины


# region Список групп шаблонов


class PatternGroupListView(PatternGroupBreadcrumbsListMixin, DynamicContentTableBaseView):
    """
    Представление: Список групп шаблонов
    """

    model = PatternGroup
    filterset_class = PatternGroupFilterSet
    table_class = PatternGroupTable
    title = 'Группы шаблонов'
    ajax_content_name = 'pattern_groups'
    action_group_classes = (PatternGroupListActionGroup,)
    filters_clear = False


# endregion Список групп шаблонов


# region Создание / редактирование групп шаблонов


class PatternGroupCreateUpdateMixin:
    """
    Миксин создания / редактирования группы шаблонов
    """

    model = PatternGroup
    form_class = PatternGroupCreateUpdateForm
    dependents = (
        ('dynamic_contents', 'pattern_groups'),
    )
    is_only_ajax = True


class PatternGroupCreateView(PatternGroupCreateUpdateMixin, CreateAjaxView):
    """
    Представление: Создание группы шаблонов
    """

    title = 'Создание группы шаблонов'


class PatternGroupUpdateView(PatternGroupCreateUpdateMixin, UpdateAjaxView):
    """
    Представление: Редактирование граппы шаблонов
    """

    title = 'Редактирование группы шаблонов'


# endregion Создание / редактирование групп шаблонов
