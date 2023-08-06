from django.db.models import (
    QuerySet,
    Prefetch,
    BooleanField,
    Value,
    When,
    Case,
    F,
)

from report_designer.choices import InternalType


class BaseIsVisibleQuerySet(QuerySet):
    """
    QuerySet видимых в констркуторе сущностей
    """

    is_visible_field = 'is_visible'

    def is_visible(self):
        """
        Видимые сущности
        """
        return self.filter(**{self.is_visible_field: True})


class TableFieldQuerySet(BaseIsVisibleQuerySet):
    """
    QuerySet полей таблиц БД
    """

    def available_for_pattern(self, pattern):
        """
        Поля доступные для шаблона
        """
        return self.is_visible().filter(db_table__patterns=pattern).distinct()

    def is_relation(self):
        """
        Поля связи
        """
        return self.filter(is_relation=True)

    def is_not_relation(self):
        """
        Поля связи
        """
        return self.filter(is_relation=False)

    def with_title(self):
        """
        Заполнение псевдонима из названия, если не указан псевдоним
        """
        return self.annotate(title=Case(When(alias__exact='', then=F('name')), default=F('alias')))


class DBTableQuerySet(BaseIsVisibleQuerySet):
    """
    QuerySet таблиц БД
    """

    def available(self, is_relation=False):
        """
        Доступные для выбора таблицы

        Таблицы попадаюбт в выборку:
        - если отображаются в конструкторе
        - если имеют поля, отображаемые в конструкторе
        """
        from report_designer.models import TableField

        tables = self.is_visible().filter(fields__is_visible=True)
        prefetch = Prefetch('fields', TableField.objects.is_visible().filter(is_relation=is_relation))
        return tables.prefetch_related(prefetch).distinct()

    def for_pattern(self, pattern):
        """
        Таблицы шаблона
        """
        root_pk = pattern.root.pk
        return (
            self.filter(patterns=pattern)
            .annotate(
                is_root_table=Case(
                    When(pk=root_pk, then=True),
                    output_field=BooleanField(),
                )
            )
            .order_by('is_root_table').distinct()
        )


class FormatQuerySet(BaseIsVisibleQuerySet):
    """
    QuerySet форматов
    """

    def available_for_field(self, table, field):
        """
        Список допустимых форматов для поля модели
        """
        choice_name = table.model_class()._meta.get_field(field).get_internal_type()
        internal_type = InternalType.get_value_by_internal_type(choice_name)
        return self.filter(internal_type=internal_type)


class PatternFieldQuerySet(QuerySet):
    """
    QuerySet полей шаблона
    """

    def with_relation(self):
        """
        Поля, имеющие связь
        """
        return self.filter(relation__isnull=False)

    def without_relation(self):
        """
        Поля, не имеющие связь
        """
        return self.filter(relation__isnull=True)

    def is_virtual(self):
        """
        Виртуальные поля
        """
        return self.filter(is_virtual=True)

    def is_group(self):
        """
        Виртуальные поля
        """
        return self.filter(is_group=True)

    def with_relation_options(self):
        """
        Поля, с аннотацией существования связи
        """
        relation_exists = Case(
            When(relation__isnull=True, then=Value(False)), default=Value(True), output_field=BooleanField()
        )
        relation_need = Case(
            When(field__db_table=F('pattern__root'), then=Value(False)),
            default=Value(True),
            output_field=BooleanField(),
        )
        return self.annotate(relation_exists=relation_exists, relation_need=relation_need)
