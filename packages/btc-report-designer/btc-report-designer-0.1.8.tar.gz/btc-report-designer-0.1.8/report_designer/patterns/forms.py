from django.forms import ModelForm

from report_designer.core.forms import StyledFormMixin
from report_designer.models import Pattern


class PatternBaseForm(StyledFormMixin, ModelForm):
    """
    Базовая форма шаблона
    """

    searching_select = (
        'root',
        'groups',
    )

    class Meta:
        model = Pattern
        fields = (
            'name',
            'groups',
            'is_visible_in_patterns',
        )


class PatternCreateForm(PatternBaseForm):
    """
    Форма: создание шаблона
    """

    class Meta(PatternBaseForm.Meta):
        fields = (
            'name',
            'root',
            'groups',
            'is_visible_in_patterns',
        )


class PatternUpdateForm(PatternBaseForm):
    """
    Форма: редактирование шаблона
    """

    pass
