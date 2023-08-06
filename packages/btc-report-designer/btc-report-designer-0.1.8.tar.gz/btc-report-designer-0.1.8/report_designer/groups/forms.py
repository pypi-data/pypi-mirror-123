from django.forms import ModelForm

from report_designer.core.forms import StyledFormMixin
from report_designer.models import PatternGroup


class PatternGroupCreateUpdateForm(StyledFormMixin, ModelForm):
    """
    Форма: создание группы шаблонов
    """

    class Meta:
        model = PatternGroup
        fields = (
            'name',
        )
