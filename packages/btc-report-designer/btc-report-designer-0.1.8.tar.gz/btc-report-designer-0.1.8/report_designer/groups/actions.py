from django.urls import reverse_lazy

from report_designer.core.actions import ActionGroup, SimpleModalAction


class PatternGroupListActionGroup(ActionGroup):
    """
    Группа действий в списке групп шаблонов
    """

    create = SimpleModalAction(title='Добавить', url=reverse_lazy('report_designer:groups:create'))
