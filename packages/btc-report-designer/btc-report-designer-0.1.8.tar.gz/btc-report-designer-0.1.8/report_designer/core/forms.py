from django.conf import settings
from django.forms import Select, NullBooleanSelect


class StyledFormMixin:
    """
    Миксин стилизации форм
    """

    js_class_prefix = 'js-rd-field'
    field_css_class = 'input__input'
    empty_choice_filter = 'Не выбрано'
    searching_select = ()
    select_id_prefix = None

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        # Поля формы
        self.form_fields = self.get_form_fields()

        # Установка базовых классов виджетов
        self.init_processing_fields()

    def init_processing_fields(self):
        """
        Обработка полей при инициализации
        """
        for field_name, field in self.form_fields.items():
            self.init_processing_field(field_name, field)

    def init_processing_field(self, field_name, field):
        """
        Обработка поля при инициализации
        """
        widget_type = field.widget.__class__.__name__.lower()
        field_classes = (
            f'{self.js_class_prefix}_{field_name}',
            f'{self.field_css_class} {self.field_css_class}_{widget_type}',
        )
        self.set_widget_class(field_name, field_classes)

        # Выпадающие списки
        if isinstance(field.widget, Select):
            # Установка пустого значения для Select
            if hasattr(field, 'empty_label') and field.empty_label is not None:
                field.empty_label = self.empty_choice_filter
            # Поиск
            if field_name in self.searching_select:
                self.set_widget_class(field_name, 'js-rd-select-search')

            # Префикс айди
            if self.select_id_prefix:
                self.add_or_update_widget_attr(field_name, 'id', f'id_{self.select_id_prefix}_{field_name}')

        # Выпадающие списки с булевыми значениями
        if isinstance(field.widget, NullBooleanSelect):
            if hasattr(settings, 'NULL_BOOLEAN_CHOICES'):
                field.widget.choices = settings.NULL_BOOLEAN_CHOICES

    def set_widget_class(self, field, value):
        """
        Установка класса виджету поля
        """
        self.add_or_update_widget_attr(field, 'class', value)

    def add_or_update_widget_attr(self, field, attr, value, joiner=' '):
        """
        Добавление или обновление аттрибута виджета поля
        """
        attrs = self.form_fields[field].widget.attrs
        value = isinstance(value, (list, tuple)) and value or [value]
        self.update_widget_attr(field, attr, f'{joiner}'.join(filter(None, [attrs.get(attr), *value])))

    def update_widget_attr(self, field, attr, value):
        """
        Обновление аттрибута виджета поля
        """
        self.form_fields[field].widget.attrs.update({attr: value})

    def get_form_fields(self):
        """
        Получение полей формы
        """
        return self.fields.copy()
