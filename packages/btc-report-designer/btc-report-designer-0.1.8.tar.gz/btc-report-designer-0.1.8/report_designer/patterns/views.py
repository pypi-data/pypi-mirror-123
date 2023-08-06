import abc

from django.db.models import (
    Value,
    F,
    BooleanField,
    Exists,
    OuterRef,
    Case,
    When,
    Q,
)
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.functional import cached_property
from django.views.generic import DetailView

from report_designer.core.views import (
    TitleMixin,
    AjaxContentListView,
    ParentMixin,
    ObjectActionAjaxView,
    DynamicContentTableBaseView,
    CreateAjaxView,
    ActionGroupMixin,
    UpdateAjaxView,
    BreadcrumbsListMixin,
    BackUrlDetailMixin,
    BreadcrumbsDetailMixin,
)
from report_designer.models import (
    Pattern,
    DBTable,
    TableField,
    PatternField,
)
from report_designer.patterns.actions import (
    PatternListActionGroup,
    PatternDropdownActionGroup,
    PatternAddFieldActionGroup,
)
from report_designer.patterns.filters import PatternFilterSet, PatternFieldsFilterSet
from report_designer.patterns.forms import PatternCreateForm, PatternUpdateForm
from report_designer.patterns.tables import PatternTable, PatternFieldsTable


# endregion Базовые миксины


class PatternBreadcrumbsListMixin(BreadcrumbsListMixin):
    """
    Хлебные крошки шаблонов
    """

    title_breadcrumb = 'Список шаблонов'


class PatternBreadcrumbsDetailBaseMixin(BreadcrumbsDetailMixin, PatternBreadcrumbsListMixin):
    """
    Хлебные крошки шаблона
    """

    pass


# endregion Базовые миксины


# region Список шаблонов


class PatternListView(PatternBreadcrumbsListMixin, DynamicContentTableBaseView):
    """
    Представление: Список шаблонов
    """

    model = Pattern
    filterset_class = PatternFilterSet
    table_class = PatternTable
    title = 'Шаблоны'
    ajax_content_name = 'patterns'
    action_group_classes = (PatternListActionGroup,)


# endregion Список шаблонов


# region Создание / редактирование шаблона


class PatternCreateUpdateMixin:
    """
    Миксин создания / редактирования шаблона
    """

    model = Pattern

    def get_success_redirect_url(self):
        return self.object.get_detail_url()


class PatternCreateView(PatternCreateUpdateMixin, CreateAjaxView):
    """
    Представление: Создание шаблона
    """

    title = 'Создание шаблона'
    form_class = PatternCreateForm

    def set_object_additional_values(self, obj):
        super().set_object_additional_values(obj)
        obj.author = self.request.user

    def after_save(self):
        super().after_save()
        self.object.tables.add(self.object.root)


class PatternUpdateView(PatternCreateUpdateMixin, UpdateAjaxView):
    """
    Представление: Редактирование шаблона
    """

    title = 'Редактирование шаблона'
    form_class = PatternUpdateForm


# endregion Создание / редактирование шаблона


# region Просмотр шаблона


class PatternDetailView(
    BackUrlDetailMixin,
    PatternBreadcrumbsDetailBaseMixin,
    ActionGroupMixin,
    TitleMixin,
    DetailView,
):
    """
    Представление: Просмотр шаблона
    """

    model = Pattern
    template_name = 'report_designer/patterns/detail.html'
    context_object_name = 'pattern'
    action_group_classes = (
        PatternDropdownActionGroup,
        PatternAddFieldActionGroup,
    )

    def get_title(self):
        return f'Шаблон "{self.object.name}"'


# endregion Просмотр шаблона


# region Редактирование списка таблиц в шаблоне


class BaseTreeListView(AjaxContentListView):
    """
    Базовое представления для вывода дерева
    """

    is_paginate = False
    is_only_ajax = True
    is_subtree = False
    template_name = 'report_designer/patterns/blocks/tree_branch.html'
    context_object_name = 'tree_branches'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data.update(
            {
                'is_subtree': self.is_subtree,
            }
        )
        return context_data


class DBTablesBaseTreeListView(ParentMixin, BaseTreeListView):
    """
    Базовое представление: Список таблиц БД / в шаблоне
    """

    queryset = DBTable.objects.available()
    context_object_name = 'tree_branches'
    parent_model = Pattern
    kwargs_parent_fk = 'pattern_pk'
    parent_context_name = 'pattern'
    is_processed = False

    def get_queryset(self):
        # Аннотация параметров для списка таблиц
        # 1). PK для URL загрузки полей
        # 2). Title из alias
        # 3). Существование связи для URL загрузки полей
        return (
            super()
            .get_queryset()
            .annotate(
                related_table_pk=F('pk'),
                title=F('alias'),
                is_relation=Value(True, output_field=BooleanField()),
            )
        )

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data.update({'action_url': self.get_action_tables_url(), 'is_processed': self.is_processed})
        return context_data

    @abc.abstractmethod
    def get_action_tables_url(self):
        """
        URL для действия с таблицами
        """
        raise NotImplementedError


class DBTablesTreeListView(DBTablesBaseTreeListView):
    """
    Представление: Список таблиц БД
    """

    def get_action_tables_url(self):
        return reverse_lazy('report_designer:patterns:add-table', kwargs={'pk': self.parent.pk})


class PatternDBTablesTreeListView(DBTablesBaseTreeListView):
    """
    Представление: Список таблиц в шаблоне
    """

    is_processed = True

    def get_queryset(self):
        # Доступны таблицы, добавленные в шаблон
        return super().get_queryset().for_pattern(self.parent)

    def get_action_tables_url(self):
        return reverse_lazy('report_designer:patterns:remove-table', kwargs={'pk': self.parent.pk})


class TableFieldsListView(ParentMixin, BaseTreeListView):
    """
    Представление: Список таблиц БД / в шаблоне
    """

    queryset = TableField.objects.none()
    parent_model = DBTable
    is_subtree = True

    def get_queryset(self):
        queryset = self.parent.fields_with_related_tables.with_title().order_by(
            'is_relation',
            'related_table_pk',
            'pk',
        )
        if self.is_processed:
            queryset = queryset.annotate(
                # is_processed_field=Exists(self.pattern.tables.filter(pk=OuterRef('db_table__pk'))),
                # todo: усточнить это и убрать при разработке условий связи
                is_processed_field=Value(True, output_field=BooleanField()),
                is_exists_in_pattern=Exists(self.pattern.pattern_fields.filter(field__pk=OuterRef('pk'))),
            )
        return queryset

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data.update(
            {
                'pattern': self.pattern,
                'is_processed': self.is_processed,
            }
        )
        return context_data

    @property
    def is_processed(self):
        """
        Переносимые поля
        """
        return 'is_processed' in self.request.GET

    @cached_property
    def pattern(self):
        """
        Шаблон
        """
        return get_object_or_404(Pattern, pk=self.kwargs.get('pattern_pk'))


class PatternDBTableChangeBaseView(ObjectActionAjaxView):
    """
    Базовое представление: Добавление / удаление таблицы в шаблоне
    """

    model = Pattern
    join_errors = True
    dependents = (('ajax_contents', 'pattern_tables'),)

    @cached_property
    def table(self):
        """
        Добавляемая таблица
        """
        return get_object_or_404(DBTable.objects.available(), pk=self.request.POST.get('table'))


class PatternDBTableAddView(PatternDBTableChangeBaseView):
    """
    Представление: Добавление таблицы в шаблон
    """

    title = 'Добавление таблицы в шаблон'

    def valid_action(self):
        is_valid = super().valid_action()
        if self.table in self.object.tables.all():
            self.add_error(f'Таблица "{self.table.alias}" уже добавлена в шаблон')
            is_valid = False
        return is_valid

    def action(self):
        super().action()
        self.object.tables.add(self.table)


class PatternDBTableRemoveView(PatternDBTableChangeBaseView):
    """
    Представление: Удаление таблицы из шаблона
    """

    title = 'Удаление таблицы из шаблона'

    def valid_action(self):
        is_valid = super().valid_action()
        if self.table not in self.object.tables.all():
            self.add_error(f'Таблица "{self.table.alias}" не существует в шаблоне')
            is_valid = False
        if self.table == self.object.root:
            self.add_error(f'Таблица "{self.table.alias}" является основной таблицей шаблона')
            is_valid = False
        return is_valid

    def action(self):
        super().action()
        self.object.tables.remove(self.table)


# endregion Редактирование списка таблиц в шаблоне


# region Список полей в шаблоне


class PatternFieldsListView(ParentMixin, DynamicContentTableBaseView):
    """
    Представление: Список полей шаблона
    """

    queryset = PatternField.objects.order_by('order')
    parent_model = Pattern
    parent_field = 'pattern'
    table_class = PatternFieldsTable
    filterset_class = PatternFieldsFilterSet
    ajax_content_name = 'pattern_fields'
    is_paginate = False

    def get_content_url_kwargs(self):
        content_url_kwargs = super().get_content_url_kwargs()
        content_url_kwargs.update(pk=self.parent.pk)
        return content_url_kwargs


class PatternFieldsAddView(ObjectActionAjaxView):
    """
    Представление: Добавление полей в шаблон
    """

    model = Pattern
    dependents = (
        ('ajax_contents', 'pattern_tables'),
        ('dynamic_contents', 'pattern_fields'),
    )

    def action(self):
        # Добавление полей в шаблон
        order = self.object.field_last_order
        PatternField.objects.bulk_create(
            [
                PatternField(
                    name=field.name,
                    alias=field.alias,
                    representation=field.representation,
                    pattern=self.object,
                    field=field,
                    order=order + index,
                )
                for index, field in enumerate(self.fields)
            ]
        )

    @cached_property
    def fields(self):
        """
        Получение полей для добавления
        """
        return TableField.objects.filter(pk__in=self.fields_ids)

    @property
    def fields_ids(self):
        """
        Список id полей из POST
        """
        return self.request.POST.getlist('selected_fields[]')


class PatternFieldChangeOrderView(ObjectActionAjaxView):
    """
    Представление: Изменение порядка поля
    """

    model = PatternField
    dependents = (('dynamic_contents', 'pattern_fields'),)

    def action(self):
        # Старое и новое значение
        old, new = self.object.order, int(self.request.POST.get('order'))
        is_downgrade = new < old

        # Обновление порядка у всех полей шаблона
        query = Case(
            *[
                When(order=Value(old), then=Value(new)),
                When(
                    Q(
                        **{
                            f'order__{is_downgrade and "l" or "g"}t': Value(old),
                            f'order__{is_downgrade and "g" or "l"}te': Value(new),
                        }
                    ),
                    then=F('order') + (is_downgrade and 1 or -1),
                ),
            ],
            default=F('order'),
        )
        self.object.pattern.pattern_fields.update(order=query)


# endregion Список полей в шаблоне
